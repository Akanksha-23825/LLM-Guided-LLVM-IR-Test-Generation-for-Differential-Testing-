import os
import sys
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from src.analytics import generate_report
# ── Setup ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "src"))

from generator import generate_ir, SEEDS
from validator import validate
from mutator import mutate_ir, MUTATION_TYPES
from repairer import repair_ir

app = Flask(__name__)

GENERATED_DIR = BASE_DIR / "testcases" / "generated"
MUTATED_DIR   = BASE_DIR / "testcases" / "mutated"
VALID_DIR     = BASE_DIR / "testcases" / "valid"
RESULTS_DIR   = BASE_DIR / "results"
REPORT_PATH   = RESULTS_DIR / "report.txt"

# Ensure folders exist
for d in [GENERATED_DIR, MUTATED_DIR, VALID_DIR, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ── Route 1 — Home ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    generated_files = sorted(
        [f.name for f in GENERATED_DIR.glob("*.ll")]
    )
    mutated_files = sorted(
        [f.name for f in MUTATED_DIR.glob("*_mut.ll")]
    )
    report_text = ""
    if REPORT_PATH.exists():
        report_text = REPORT_PATH.read_text(encoding="utf-8")

    return render_template(
        "index.html",
        generated_files=generated_files,
        mutated_files=mutated_files,
        report_text=report_text,
        seeds=SEEDS,
        mutation_types=MUTATION_TYPES,
    )


# ── Route 2 — Generate ─────────────────────────────────────────────────────────
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    seed = (data or {}).get("seed", "").strip()
    if not seed:
        return jsonify({"error": "seed is required"}), 400

    try:
        ir_text = generate_ir(seed)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    save_path = GENERATED_DIR / "gen_custom.ll"
    save_path.write_text(ir_text, encoding="utf-8")

    result = validate(str(save_path))
    return jsonify({
        "ir":     ir_text,
        "valid":  result["valid"],
        "errors": result["errors"],
    })


# ── Route 3 — Validate ─────────────────────────────────────────────────────────
@app.route("/validate", methods=["POST"])
def validate_file():
    data     = request.get_json()
    filename = (data or {}).get("filename", "").strip()
    if not filename:
        return jsonify({"error": "filename is required"}), 400

    filepath = GENERATED_DIR / filename
    if not filepath.exists():
        return jsonify({"error": f"File not found: {filename}"}), 404

    result   = validate(str(filepath))
    ir_text  = filepath.read_text(encoding="utf-8")
    return jsonify({
        "valid":  result["valid"],
        "errors": result["errors"],
        "ir":     ir_text,
    })


# ── Route 4 — Mutate ───────────────────────────────────────────────────────────
@app.route("/mutate", methods=["POST"])
def mutate():
    data          = request.get_json()
    filename      = (data or {}).get("filename", "").strip()
    mutation_type = (data or {}).get("mutation_type", "").strip()

    if not filename:
        return jsonify({"error": "filename is required"}), 400
    if not mutation_type:
        mutation_type = MUTATION_TYPES[0]

    filepath = GENERATED_DIR / filename
    if not filepath.exists():
        return jsonify({"error": f"File not found: {filename}"}), 404

    original_ir = filepath.read_text(encoding="utf-8")

    try:
        mutated_ir = mutate_ir(original_ir, mutation_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    stem      = Path(filename).stem
    save_path = MUTATED_DIR / f"{stem}_mut_custom.ll"
    save_path.write_text(mutated_ir, encoding="utf-8")

    result = validate(str(save_path))
    return jsonify({
        "original_ir":   original_ir,
        "mutated_ir":    mutated_ir,
        "valid":         result["valid"],
        "mutation_type": mutation_type,
    })


# ── Route 5 — Repair ───────────────────────────────────────────────────────────
@app.route("/repair", methods=["POST"])
def repair():
    data     = request.get_json()
    filename = (data or {}).get("filename", "").strip()
    if not filename:
        return jsonify({"error": "filename is required"}), 400

    filepath = GENERATED_DIR / filename
    if not filepath.exists():
        return jsonify({"error": f"File not found: {filename}"}), 404

    validation   = validate(str(filepath))
    errors       = validation["errors"]
    original_ir  = filepath.read_text(encoding="utf-8")

    try:
        repaired_ir = repair_ir(original_ir, errors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    stem          = Path(filename).stem
    repaired_path = GENERATED_DIR / f"{stem}_repaired.ll"
    repaired_path.write_text(repaired_ir, encoding="utf-8")

    recheck = validate(str(repaired_path))
    return jsonify({
        "original_ir": original_ir,
        "repaired_ir": repaired_ir,
        "fixed":       recheck["valid"],
        "errors":      errors,
    })


# ── Route 6 — Run Pipeline ─────────────────────────────────────────────────────
@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        proc = subprocess.run(
            [sys.executable, "src/pipeline.py"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ},
        )
        output  = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
        success = proc.returncode == 0
    except subprocess.TimeoutExpired:
        output  = "Pipeline timed out after 5 minutes."
        success = False
    except Exception as e:
        output  = str(e)
        success = False

    return jsonify({"output": output, "success": success})


# ── Route 7 — Diff Report ──────────────────────────────────────────────────────
@app.route("/diff_report")
def diff_report():
    if not REPORT_PATH.exists():
        return jsonify({
            "report":      "No report found. Run the pipeline first.",
            "pass_count":  0,
            "diff_count":  0,
            "error_count": 0,
        })

    report_text = REPORT_PATH.read_text(encoding="utf-8")

    pass_count  = report_text.count("[PASS]")
    diff_count  = report_text.count("[DIFF]")
    error_count = report_text.count("[ERROR]")

    # Also try to parse the summary line: PASS=X  DIFF=Y  ERROR=Z
    import re
    summary = re.search(r"PASS=(\d+)\s+DIFF=(\d+)\s+ERROR=(\d+)", report_text)
    if summary:
        pass_count  = int(summary.group(1))
        diff_count  = int(summary.group(2))
        error_count = int(summary.group(3))

    return jsonify({
        "report":      report_text,
        "pass_count":  pass_count,
        "diff_count":  diff_count,
        "error_count": error_count,
    })


# ── Route 8 — List Test Cases ──────────────────────────────────────────────────
@app.route("/testcases")
def list_testcases():
    files = []

    for directory, category in [(GENERATED_DIR, "generated"), (MUTATED_DIR, "mutated")]:
        for filepath in sorted(directory.glob("*.ll")):
            try:
                content    = filepath.read_text(encoding="utf-8", errors="replace")
                first_line = content.splitlines()[0] if content.strip() else ""
            except Exception:
                first_line = ""

            files.append({
                "name":       filepath.name,
                "category":   category,
                "size_bytes": filepath.stat().st_size,
                "first_line": first_line,
            })

    return jsonify(files)


# ── Route 9 — Re-run Diff Test ────────────────────────────────────────────────
@app.route("/run_diff", methods=["POST"])
def run_diff():

    try:

        proc = subprocess.run(
            [
                sys.executable,
                "diff_tester.py",
                "--report",
                "results/report.txt"
            ],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300
        )

        output = proc.stdout

        if proc.stderr:
            output += "\n" + proc.stderr

        success = proc.returncode == 0

    except subprocess.TimeoutExpired:

        output = "Differential testing timed out."
        success = False

    except Exception as e:

        output = str(e)
        success = False

    return jsonify({
        "success": success,
        "output": output
    })

# ==========================================
# ANALYTICS ROUTE
# ==========================================

@app.route("/analytics")
def analytics():

    try:
        report = generate_report()

        return jsonify({
            "success": True,
            "data": report
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# ==========================================
# START FLASK
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)