from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).parent.parent

GENERATED_DIR = BASE_DIR / "testcases" / "generated"
MUTATED_DIR = BASE_DIR / "testcases" / "mutated"
VALID_DIR = BASE_DIR / "testcases" / "valid"

REPORT_FILE = BASE_DIR / "results" / "report.txt"


def categorize_error(error_text):

    error_text = error_text.lower()

    if "phi" in error_text:
        return "PHI Error"

    if "ssa" in error_text or "multiple definition" in error_text:
        return "SSA Error"

    if "undefined value" in error_text:
        return "Undefined Value"

    if "expected 'i32'" in error_text:
        return "Type Error"

    if "terminator" in error_text:
        return "Missing Terminator"

    return "Syntax Error"


def get_pipeline_stats():

    generated_files = [
    f for f in GENERATED_DIR.glob("gen_*.ll")
    if "_repaired" not in f.name
]

    valid_files = list(VALID_DIR.glob("*.ll"))

    mutated_files = list(MUTATED_DIR.glob("*.ll"))

    generated_count = len(
        [f for f in generated_files
         if "_repaired" not in f.name]
    )

    valid_count = len(valid_files)

    invalid_count = max(
        generated_count - valid_count,
        0
    )

    validity_rate = round(
        (valid_count / generated_count) * 100,
        2
    ) if generated_count else 0

    mutation_count = len(mutated_files)

    mutation_rate = round(
        (mutation_count / valid_count) * 100,
        2
    ) if valid_count else 0

    return {
        "generated": generated_count,
        "valid": valid_count,
        "invalid": invalid_count,
        "validity_rate": validity_rate,
        "mutations": mutation_count,
        "mutation_rate": mutation_rate
    }


def get_diff_stats():

    if not REPORT_FILE.exists():

        return {
            "pass": 0,
            "diff": 0,
            "error": 0
        }

    text = REPORT_FILE.read_text()

    pass_count = len(
        re.findall(r"\[PASS\]", text)
    )

    diff_count = len(
        re.findall(r"\[DIFF\]", text)
    )

    error_count = len(
        re.findall(r"\[ERROR\]", text)
    )

    return {
        "pass": pass_count,
        "diff": diff_count,
        "error": error_count
    }


def get_diversity_stats():

    categories = {
        "Arithmetic": 0,
        "Loops": 0,
        "Bitwise": 0,
        "PHI": 0,
        "Advanced": 0,
        "ControlFlow": 0
    }

    for file in GENERATED_DIR.glob("gen_*.ll"):

        text = file.read_text().lower()

        if "add" in text or "sub" in text or "mul" in text:
            categories["Arithmetic"] += 1

        if "br label" in text and "icmp" in text:
            categories["ControlFlow"] += 1

        if "phi" in text:
            categories["PHI"] += 1

        if "xor" in text or "and" in text or "shl" in text:
            categories["Bitwise"] += 1

        if "loop" in text:
            categories["Loops"] += 1

        if "gcd" in text or "power" in text or "fizz" in text:
            categories["Advanced"] += 1

    return categories


def generate_report():

    stats = get_pipeline_stats()

    diff = get_diff_stats()

    diversity = get_diversity_stats()

    report = {
        "pipeline": stats,
        "differential_testing": diff,
        "diversity": diversity
    }

    output_file = (
        BASE_DIR /
        "results" /
        "analytics.json"
    )

    with open(output_file, "w") as f:
        json.dump(
            report,
            f,
            indent=4
        )

    return report


if __name__ == "__main__":

    report = generate_report()

    print("\n=== ANALYTICS REPORT ===\n")

    print(
        f"Generated      : "
        f"{report['pipeline']['generated']}"
    )

    print(
        f"Valid          : "
        f"{report['pipeline']['valid']}"
    )

    print(
        f"Invalid        : "
        f"{report['pipeline']['invalid']}"
    )

    print(
        f"Validity Rate  : "
        f"{report['pipeline']['validity_rate']}%"
    )

    print()

    print(
        f"PASS           : "
        f"{report['differential_testing']['pass']}"
    )

    print(
        f"DIFF           : "
        f"{report['differential_testing']['diff']}"
    )

    print(
        f"ERROR          : "
        f"{report['differential_testing']['error']}"
    )

    print()

    print("=== DIVERSITY ===")

    for k, v in report["diversity"].items():
        print(f"{k:<15}: {v}")

    print(
        "\nAnalytics saved to "
        "results/analytics.json"
    )