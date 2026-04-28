
import os
import re
import subprocess
import sys

SSA_DEF_RE = re.compile(r"^\s*(%[\w.\-]+)\s*=")
LABEL_RE = re.compile(r"^\s*([\w.\-]+):\s*(?:;.*)?$")
PHI_RE = re.compile(r"\bphi\b")
PHI_LABEL_RE = re.compile(r"\[\s*.*?\s*,\s*%?([\w.\-]+)\s*\]")
TERMINATORS = ("ret", "br", "switch", "unreachable")


def run_opt_verify(filepath):
    result = subprocess.run(
        ["opt", "-passes=verify", "-S", filepath, "-o", "/dev/null"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, (result.stderr or "").strip() or "opt --verify failed"
    return True, ""


def split_functions(lines):
    functions = []
    current = []
    in_function = False
    brace_depth = 0

    for line in lines:
        stripped = line.lstrip()

        if not in_function and stripped.startswith("define"):
            current = [line]
            in_function = True
            brace_depth = line.count("{") - line.count("}")
            if brace_depth <= 0:
                functions.append(current)
                current = []
                in_function = False
            continue

        if in_function:
            current.append(line)
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                functions.append(current)
                current = []
                in_function = False

    return functions


def check_ssa(lines):
    errors = []
    definitions = {}

    for line in lines:
        match = SSA_DEF_RE.match(line)
        if not match:
            continue

        name = match.group(1)
        if name in definitions:
            errors.append(f"SSA violation: {name} defined more than once")
        else:
            definitions[name] = True

    return errors


def split_blocks(function_lines):
    blocks = []
    current_label = None
    current_lines = []
    saw_function_start = False

    for line in function_lines:
        stripped = line.strip()

        if not saw_function_start:
            if "{" in line:
                saw_function_start = True
                current_label = "entry"
            continue

        if stripped in ("", "{", "}"):
            continue

        label_match = LABEL_RE.match(line)
        if label_match:
            label_name = label_match.group(1)
            if current_label is not None and current_lines:
                blocks.append((current_label, current_lines))

            if label_name == "entry" and not blocks and not current_lines:
                current_label = "entry"
                current_lines = []
            else:
                current_label = label_name
                current_lines = []
            continue

        if current_label is not None:
            current_lines.append(line)

    if current_label is not None and current_lines:
        blocks.append((current_label, current_lines))

    return blocks


def last_relevant_line(block_lines):
    for line in reversed(block_lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in ("{", "}"):
            continue
        if stripped.startswith(";"):
            continue
        if LABEL_RE.match(line):
            continue
        return stripped
    return ""


def check_terminators(functions):
    errors = []

    for function_lines in functions:
        for _, block_lines in split_blocks(function_lines):
            last_line = last_relevant_line(block_lines)
            if not last_line or not last_line.startswith(TERMINATORS):
                errors.append("Missing terminator in block")

    return errors


def check_phi_nodes(functions):
    errors = []

    for function_lines in functions:
        block_names = {label for label, _ in split_blocks(function_lines)}

        for line in function_lines:
            if not PHI_RE.search(line):
                continue

            for label in PHI_LABEL_RE.findall(line):
                if label not in block_names:
                    errors.append(f"PHI references undefined label: {label}")

    return errors


def validate(filepath):
    errors = []

    ok, opt_error = run_opt_verify(filepath)
    if not ok:
        errors.append(opt_error)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as exc:
        return {
            "file": filepath,
            "valid": False,
            "errors": [f"Failed to read file: {exc}"],
        }

    lines = text.splitlines()
    functions = split_functions(lines)

    errors.extend(check_ssa(lines))
    errors.extend(check_terminators(functions))
    errors.extend(check_phi_nodes(functions))

    return {
        "file": filepath,
        "valid": len(errors) == 0,
        "errors": errors,
    }


if __name__ == "__main__":
    for filepath in sys.argv[1:]:
        result = validate(filepath)
        filename = os.path.basename(result["file"])

        if result["valid"]:
            print(f"✅ VALID: {filename}")
        else:
            print(f"❌ INVALID: {filename}")
            for error in result["errors"]:
                print(f"  → {error}")
