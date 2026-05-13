import os
import sys
import shutil
import random
import subprocess
from pathlib import Path

# Add src/ to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Base project directory
BASE_DIR = Path(__file__).parent.parent

# Create required folders
GENERATED_DIR = BASE_DIR / "testcases" / "generated"
MUTATED_DIR = BASE_DIR / "testcases" / "mutated"
VALID_DIR = BASE_DIR / "testcases" / "valid"
RESULTS_DIR = BASE_DIR / "results"

GENERATED_DIR.mkdir(parents=True, exist_ok=True)
MUTATED_DIR.mkdir(parents=True, exist_ok=True)
VALID_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Import project modules
from generator import SEEDS, generate_ir
from validator import validate
from repairer import repair_ir
from mutator import MUTATION_TYPES, mutate_ir


def main():
    valid_files = []
    invalid_files = []
    repair_success = 0
    mut_valid = 0

    # =========================================================
    # STEP 1 — Generate IR
    # =========================================================
    print("\n=== STEP 1: Generating IR ===")

    for i, seed in enumerate(SEEDS):
        ir_text = generate_ir(seed)

        filepath = GENERATED_DIR / f"gen_{i}.ll"

        with open(filepath, "w") as f:
            f.write(ir_text)

        print(f"  Saved gen_{i}.ll")

    # =========================================================
    # STEP 2 — Validate
    # =========================================================
    print("\n=== STEP 2: Validating Generated IR ===")

    for i in range(10):
        filepath = GENERATED_DIR / f"gen_{i}.ll"

        result = validate(filepath)

        if result["valid"]:
            print(f"  ✅ VALID: gen_{i}.ll")

            shutil.copy(filepath, VALID_DIR / filepath.name)

            valid_files.append(filepath)

        else:
            print(f"  ❌ INVALID: gen_{i}.ll")

            for err in result["errors"]:
                print(f"    → {err}")

            invalid_files.append((filepath, result["errors"]))

    # =========================================================
    # STEP 3 — Repair Invalid IR
    # =========================================================
    print("\n=== STEP 3: Repairing Invalid IR ===")

    for path, errors in invalid_files:
        with open(path, "r") as f:
            ir_text = f.read()

        repaired_ir = repair_ir(ir_text, errors)

        repaired_path = path.parent / f"{path.stem}_repaired.ll"

        with open(repaired_path, "w") as f:
            f.write(repaired_ir)

        repair_result = validate(repaired_path)

        if repair_result["valid"]:
            print(f"  ✅ Repaired successfully: {repaired_path.name}")
            repair_success += 1
        else:
            print(f"  ❌ Repair failed: {repaired_path.name}")

    # =========================================================
    # STEP 4 — Mutate Valid Files
    # =========================================================
    print("\n=== STEP 4: Mutating Valid IR ===")

    for path in valid_files:
        with open(path, "r") as f:
            ir_text = f.read()

        mutation_type = random.choice(MUTATION_TYPES)

        mutated_ir = mutate_ir(ir_text, mutation_type)

        mutated_path = MUTATED_DIR / f"{path.stem}_mut.ll"

        with open(mutated_path, "w") as f:
            f.write(mutated_ir)

        mutation_result = validate(mutated_path)

        if mutation_result["valid"]:
            print(f"  ✅ Mutation valid: {mutated_path.name}")
            mut_valid += 1
        else:
            print(f"  ⚠️  Mutation invalid: {mutated_path.name}")

    # =========================================================
    # STEP 5 — Differential Testing
    # =========================================================
    print("\n=== STEP 5: Running Differential Testing ===")

    try:
        subprocess.run(
            ["python3", "diff_tester.py", "--report", "results/report.txt"],
            cwd=BASE_DIR,
            capture_output=False
        )

    except Exception as e:
        print(f"Error running differential testing: {e}")

    # =========================================================
    # STEP 6 — Final Summary
    # =========================================================
    print("\n=== PIPELINE COMPLETE ===")
    print(f"Files generated   : 10")
    print(f"Valid             : {len(valid_files)}")
    print(f"Invalid           : {len(invalid_files)}")
    print(f"Repaired          : {repair_success} / {len(invalid_files)}")
    print(f"Mutations valid   : {mut_valid} / {len(valid_files)}")
    print(f"Diff test report  : results/report.txt")


if __name__ == "__main__":
    main()