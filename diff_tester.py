#!/usr/bin/env python3
"""
diff_tester.py  —  Differential Testing: -O0 vs -O2 vs -O3
===========================================================
Each IR file defines a function with NO main(). This script:
  1. Parses the function name + signature from the .ll file
  2. Pre-validates / repairs known IR issues before compiling
  3. Generates a C main() wrapper with fixed test inputs
  4. Compiles IR + wrapper at -O0, -O2, -O3
  5. Compares printed output — DIFF = optimiser changed behaviour

Usage (run from "Compiler Design" folder):
  python3 diff_tester.py
  python3 diff_tester.py --gen-only
  python3 diff_tester.py --mut-only
  python3 diff_tester.py --report results/report.txt
"""

import argparse, os, re, subprocess, sys, tempfile
from pathlib import Path

OPT_LEVELS      = ["-O0", "-O2", "-O3"]
TIMEOUT_COMPILE = 30
TIMEOUT_RUN     = 10

VALID_FILES = [
    "testcases/generated/gen_0.ll",
    "testcases/generated/gen_2.ll",
    "testcases/generated/gen_3.ll",
    "testcases/generated/gen_5.ll",
    "testcases/generated/gen_6.ll",
    "testcases/generated/gen_8.ll",
    "testcases/generated/gen_9.ll",
]

# Test inputs per function — multiple calls, results printed line by line
TEST_INPUTS = {
    "add":       [(3, 4), (10, 20), (0, 0), (-1, 1)],
    "even":      [(4,), (7,), (0,), (1,)],
    "factorial": [(5,), (1,), (6,), (3,)],
    "multiply":  [(3, 4), (6, 7), (0, 5), (-2, 3)],
    "subtract":  [(10, 3), (5, 5), (0, 1), (-1, -1)],
    "sum_loop":  [(5,), (10,), (1,), (3,)],
    "min":       [(3, 7), (9, 2), (4, 4), (-1, 0)],
}

# ── colours ───────────────────────────────────────────────────────────────────
def _c(code, s): return f"\033[{code}m{s}\033[0m"
def green(s):  return _c(92, s)
def red(s):    return _c(91, s)
def yellow(s): return _c(93, s)
def cyan(s):   return _c(96, s)
def bold(s):   return _c(1,  s)

# ── find clang ────────────────────────────────────────────────────────────────
def find_clang():
    for name in ["clang","clang-20","clang-19","clang-18","clang-17","clang-16"]:
        r = subprocess.run(["which", name], capture_output=True, text=True)
        if r.returncode == 0:
            return name.strip()
    return None

# ── parse IR: get function name and arg count ─────────────────────────────────
def parse_ir(ir_path):
    text = Path(ir_path).read_text(errors="replace")
    m = re.search(r'define\s+\w+\s+@(\w+)\s*\(([^)]*)\)', text)
    if not m:
        return None, 0
    func_name = m.group(1)
    params    = m.group(2).strip()
    n_args    = 0 if params == "" else len(params.split(","))
    return func_name, n_args

# ── IR pre-repair: fix known issues before handing to clang ───────────────────
def repair_ir(ir_text):
    """
    Fix SSA numbering order issues in LLM-mutated IR.

    LLVM rule: numbered temporaries (%1, %2, ...) must be defined in
    strictly increasing order as they appear in the source text.

    The mutator sometimes inserts a new %N in the middle of a block
    where N is LESS than a %M defined later (e.g. inserts %9 before %8).
    Clang rejects this. Fix: scan top-to-bottom, if a definition's
    number is <= the current maximum, push it above the maximum.
    All uses of that number are updated accordingly.
    """
    lines = ir_text.splitlines()

    # Collect definition order
    defs_in_order = []
    for line in lines:
        m = re.match(r'\s*%(\d+)\s*=', line)
        if m:
            defs_in_order.append(int(m.group(1)))

    # Build remap: only renumber definitions that are out of order
    remap    = {}
    max_seen = 0
    for num in defs_in_order:
        mapped = remap.get(num, num)
        if mapped <= max_seen:
            new_num      = max_seen + 1
            remap[num]   = new_num
            max_seen     = new_num
        else:
            max_seen = mapped

    if not remap:
        return ir_text  # nothing to fix

    result = []
    for line in lines:
        def sub(m):
            n = int(m.group(1))
            return f'%{remap.get(n, n)}'
        line = re.sub(r'%(\d+)', sub, line)
        result.append(line)
    return "\n".join(result)

# ── generate C wrapper ────────────────────────────────────────────────────────
def make_wrapper(func_name, n_args):
    inputs = TEST_INPUTS.get(func_name, [tuple([0]*n_args)])
    calls  = []
    for args in inputs:
        if len(args) != n_args:
            continue
        args_str = ", ".join(str(a) for a in args)
        calls.append(f'    printf("%d\\n", {func_name}({args_str}));')
    if not calls:
        args_str = ", ".join(["0"]*n_args)
        calls.append(f'    printf("%d\\n", {func_name}({args_str}));')
    params_decl = ", ".join(["int"]*n_args)
    body        = "\n".join(calls)
    return f"""\
#include <stdio.h>
extern int {func_name}({params_decl});
int main(void) {{
{body}
    return 0;
}}
"""

# ── compile ───────────────────────────────────────────────────────────────────
def compile_ir(clang, ir_path, wrapper_c, opt_level, out_path):
    strategies = [
        ["-Wno-override-module", "-Wno-error"],
        ["-Wno-override-module", "-Wno-error", "-Xclang", "-no-opaque-pointers"],
        ["-Wno-override-module"],
        [],
    ]
    last_err = ""
    for extra in strategies:
        cmd = [clang, opt_level] + extra + [ir_path, wrapper_c, "-o", out_path, "-lm"]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_COMPILE)
            if r.returncode == 0:
                return True, r.stderr.strip()
            last_err = r.stderr.strip()
            if "unknown argument" in last_err or "invalid value" in last_err:
                continue
            return False, last_err
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out"
        except FileNotFoundError:
            return False, f"Compiler '{clang}' not found"
    return False, last_err

# ── run ───────────────────────────────────────────────────────────────────────
def run_binary(path):
    try:
        r = subprocess.run([path], capture_output=True, text=True, timeout=TIMEOUT_RUN)
        return r.stdout.strip(), r.returncode, None
    except subprocess.TimeoutExpired:
        # Timeout itself IS an observable result — record it
        return "TIMEOUT", -99, None
    except Exception as e:
        return "", -1, str(e)

# ── test one file ─────────────────────────────────────────────────────────────
def test_file(clang, ir_path):
    func_name, n_args = parse_ir(ir_path)
    if func_name is None:
        return {"file": ir_path, "status": "ERROR", "func": "?",
                "details": ["  Could not parse function from IR"], "divergences": []}

    wrapper_src = make_wrapper(func_name, n_args)
    results     = {}

    with tempfile.TemporaryDirectory() as tmp:
        # Apply IR repair (fix SSA numbering gaps)
        original_text = Path(ir_path).read_text(errors="replace")
        repaired_text = repair_ir(original_text)
        repaired_ir   = os.path.join(tmp, "repaired.ll")
        with open(repaired_ir, "w") as f:
            f.write(repaired_text)

        wrapper_c = os.path.join(tmp, "main_wrapper.c")
        with open(wrapper_c, "w") as f:
            f.write(wrapper_src)

        was_repaired = repaired_text != original_text

        for opt in OPT_LEVELS:
            out = os.path.join(tmp, f"prog_{opt[1:]}")
            ok, err = compile_ir(clang, repaired_ir, wrapper_c, opt, out)
            if not ok:
                results[opt] = {"ok": False, "stdout": "", "rc": -1, "err": err}
                continue
            stdout, rc, run_err = run_binary(out)
            results[opt] = {"ok": True, "stdout": stdout, "rc": rc, "err": run_err}

    details = [f"  Function: @{func_name}({n_args} args)"]
    if was_repaired:
        details.append("  [Note: SSA numbering gap repaired before compile]")

    for opt, r in results.items():
        if not r["ok"]:
            details.append(f"  {opt}: COMPILE FAILED — {r['err'][:120]}")
        elif r["err"]:
            details.append(f"  {opt}: RUNTIME ERROR  — {r['err']}")
        else:
            details.append(f"  {opt}: output = {r['stdout']!r}")

    good = {opt: r for opt, r in results.items() if r["ok"] and not r["err"]}
    if not good:
        return {"file": ir_path, "status": "ERROR", "details": details,
                "divergences": [], "func": func_name}

    baseline_opt = list(good)[0]
    base         = good[baseline_opt]
    divergences  = []

    for opt, r in list(good.items())[1:]:
        if r["stdout"] != base["stdout"] or r["rc"] != base["rc"]:
            parts = []
            if r["rc"] != base["rc"]:
                parts.append(f"exit {base['rc']}({baseline_opt}) != {r['rc']}({opt})")
            if r["stdout"] != base["stdout"]:
                parts.append(
                    f"\n    {baseline_opt} output: {base['stdout']!r}"
                    f"\n    {opt} output:  {r['stdout']!r}"
                )
            divergences.append("  >> DIVERGENCE: " + " | ".join(parts))

    compile_fails = [opt for opt, r in results.items() if not r["ok"]]
    if compile_fails and not divergences:
        return {"file": ir_path, "status": "ERROR", "details": details,
                "divergences": [], "func": func_name}

    return {"file": ir_path,
            "status": "DIFF" if divergences else "PASS",
            "details": details, "divergences": divergences, "func": func_name}

# ── printing ──────────────────────────────────────────────────────────────────
ICON = {"PASS": "[PASS]", "DIFF": "[DIFF]", "ERROR": "[ERROR]"}
CLR  = {"PASS": green, "DIFF": red, "ERROR": yellow}

def print_result(r, quiet=False):
    name = os.path.basename(r["file"])
    print(CLR[r["status"]](f"{ICON[r['status']]}  {name}"))
    if not quiet or r["status"] != "PASS":
        for line in r["details"]: print(line)
        for div  in r["divergences"]: print(red(div))
    print()

def print_summary(all_results):
    total  = len(all_results)
    passed = sum(1 for r in all_results if r["status"] == "PASS")
    diffs  = sum(1 for r in all_results if r["status"] == "DIFF")
    errors = sum(1 for r in all_results if r["status"] == "ERROR")
    print(bold("=" * 58))
    print(bold("SUMMARY"))
    print(bold("=" * 58))
    print(f"  Total files tested : {total}")
    print(green(f"  PASS               : {passed}"))
    print(red(  f"  DIFF (divergences) : {diffs}   <- optimiser changed behaviour"))
    print(yellow(f"  ERROR              : {errors}"))
    if diffs:
        print()
        print(red(bold("Files with divergence (interesting findings!):")))
        for r in all_results:
            if r["status"] == "DIFF":
                print(red(f"  * {r['file']}"))
                for div in r["divergences"]: print(div)

def save_report(all_results, path):
    lines = ["Differential Testing Report", "=" * 58]
    for r in all_results:
        lines.append(f"\n[{r['status']}] {r['file']}")
        lines.extend(r["details"])
        lines.extend(r["divergences"])
    passed = sum(1 for r in all_results if r["status"] == "PASS")
    diffs  = sum(1 for r in all_results if r["status"] == "DIFF")
    errors = sum(1 for r in all_results if r["status"] == "ERROR")
    lines += ["", "=" * 58, f"PASS={passed}  DIFF={diffs}  ERROR={errors}"]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write("\n".join(lines))
    print(cyan(f"\nReport saved -> {path}"))

def collect_files(args):
    if args.files: return args.files
    base = Path(__file__).parent
    files = []
    if not args.mut_only:
        for rel in VALID_FILES:
            p = base / rel
            if p.exists(): files.append(str(p))
            else: print(yellow(f"WARNING: not found: {p}"))
    if not args.gen_only:
        mut_dir = base / "testcases" / "mutated"
        if mut_dir.exists():
            for p in sorted(mut_dir.glob("*_mut.ll")): files.append(str(p))
        else: print(yellow("WARNING: mutated/ not found"))
    return files

def main():
    parser = argparse.ArgumentParser(description="Differential tester: -O0/-O2/-O3")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--gen-only", action="store_true")
    parser.add_argument("--mut-only", action="store_true")
    parser.add_argument("--quiet",    action="store_true")
    parser.add_argument("--report",   metavar="FILE")
    args = parser.parse_args()

    clang = find_clang()
    if clang is None:
        print(red("\nERROR: clang not found.\nInstall: sudo apt-get install clang\n"))
        sys.exit(1)

    ver      = subprocess.run([clang, "--version"], capture_output=True, text=True)
    ver_line = ver.stdout.splitlines()[0] if ver.stdout else "unknown"
    print(cyan(f"Compiler  : {clang}  ({ver_line})"))
    print(cyan(f"Opt levels: {' | '.join(OPT_LEVELS)}"))
    print()

    files = collect_files(args)
    if not files:
        print(yellow("No .ll files found. Run from 'Compiler Design' folder."))
        sys.exit(1)

    print(bold(f"Testing {len(files)} file(s)...\n"))
    all_results = []
    for ir in files:
        r = test_file(clang, ir)
        all_results.append(r)
        print_result(r, quiet=args.quiet)

    print_summary(all_results)
    if args.report: save_report(all_results, args.report)

    if any(r["status"] == "DIFF"  for r in all_results): sys.exit(1)
    if all(r["status"] == "ERROR" for r in all_results): sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
