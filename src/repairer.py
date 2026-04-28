
# pip install groq

import glob
import os

from groq import Groq

from validator import validate

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

REPAIR_SYSTEM_PROMPT = """You are an LLVM IR repair engine.
Fix only the specific errors listed, keep everything else unchanged.
For PHI node errors: fix predecessor labels to match actual blocks.
For type mismatches: add zext or sext cast to make types match.
For numbering errors: renumber variables sequentially from %1.
Output corrected raw LLVM IR only, no markdown, no explanation."""


def strip_markdown(text):
    cleaned = text.strip()

    if cleaned.startswith("```llvm"):
        cleaned = cleaned[len("```llvm") :].lstrip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```") :].lstrip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].rstrip()

    return cleaned


def repair_ir(invalid_ir, errors):
    formatted_errors = "\n".join(
        f"{index}. {error}" for index, error in enumerate(errors, start=1)
    )

    user_message = (
        "Repair the following LLVM IR using only the listed errors.\n\n"
        f"Errors:\n{formatted_errors}\n\n"
        f"Invalid LLVM IR:\n{invalid_ir}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": REPAIR_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    text = response.choices[0].message.content or ""
    return strip_markdown(text)


if __name__ == "__main__":
    input_pattern = os.path.join("testcases", "generated", "*.ll")
    total_invalid = 0
    total_fixed = 0

    for filepath in sorted(glob.glob(input_pattern)):
        result = validate(filepath)
        if result["valid"]:
            continue

        total_invalid += 1
        filename = os.path.basename(filepath)

        print(f"Repairing {filename}...")
        if result["errors"]:
            print(f"Errors: {result['errors'][0]}")
        else:
            print("Errors: Unknown validation error")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                invalid_ir = f.read()

            repaired_ir = repair_ir(invalid_ir, result["errors"])

            base_name, _ = os.path.splitext(filepath)
            repaired_path = f"{base_name}_repaired.ll"

            with open(repaired_path, "w", encoding="utf-8") as f:
                f.write(repaired_ir)

            repaired_name = os.path.basename(repaired_path)
            print(f"→ Saved to {repaired_name}")

            recheck = validate(repaired_path)
            if recheck["valid"]:
                total_fixed += 1
                print("→ Re-validation: ✅ FIXED")
            else:
                print("→ Re-validation: ❌ STILL INVALID")
        except Exception as exc:
            print(f"→ Re-validation: ❌ STILL INVALID")
            print(f"→ Error: {exc}")

    if total_invalid == 0:
        print("Repair success rate: 0/0 (0.00%)")
    else:
        percentage = (total_fixed / total_invalid) * 100
        print(
            f"Repair success rate: {total_fixed}/{total_invalid} ({percentage:.2f}%)"
        )
