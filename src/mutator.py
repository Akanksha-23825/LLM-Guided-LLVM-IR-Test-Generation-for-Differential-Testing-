# pip install groq

import glob
import os
import random

from groq import Groq

from validator import validate

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

MUTATOR_SYSTEM_PROMPT = """You are an LLVM IR mutation engine.
Apply exactly ONE mutation to the given IR.
Output must still be valid LLVM IR.
Never break SSA form, terminators, or type consistency.
Add comment on line 1: ; Mutation: describe what was changed
Output raw LLVM IR only, no markdown, no explanation."""

MUTATION_TYPES = [
    "replace a numeric constant with a different constant value",
    "swap one arithmetic operator: change add to mul or sub to add",
    "add one dead computation whose result is never used",
    "rename one SSA variable consistently everywhere it appears",
]


def strip_markdown(text):
    cleaned = text.strip()

    if cleaned.startswith("```llvm"):
        cleaned = cleaned[len("```llvm") :].lstrip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```") :].lstrip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].rstrip()

    return cleaned


def mutate_ir(original_ir, mutation_type):
    user_prompt = (
        f"Apply this mutation type: {mutation_type}\n\n"
        f"LLVM IR to mutate:\n{original_ir}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": MUTATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.6,
    )

    text = response.choices[0].message.content or ""
    return strip_markdown(text)


if __name__ == "__main__":
    input_pattern = os.path.join("testcases", "generated", "*.ll")
    output_dir = os.path.join("testcases", "mutated")
    os.makedirs(output_dir, exist_ok=True)

    for filepath in sorted(glob.glob(input_pattern)):
        result = validate(filepath)
        if not result["valid"]:
            continue

        mutation_type = random.choice(MUTATION_TYPES)
        filename = os.path.basename(filepath)
        print(f"Mutating {filename} with: {mutation_type}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                original_ir = f.read()

            mutated_ir = mutate_ir(original_ir, mutation_type)

            base_name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{base_name}_mut.ll")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(mutated_ir)

            preview = mutated_ir.splitlines()[0] if mutated_ir.splitlines() else ""
            print(preview)
        except Exception as exc:
            print(f"Error mutating {filename}: {exc}")
