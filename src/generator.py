# pip install groq

import os

from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an LLVM IR code generator.
Use SSA form: every variable like %x is defined exactly once, never redefined.
Every basic block must end with a terminator: ret, br, switch, or unreachable.
The first basic block must always be labeled entry:
PHI nodes must list every predecessor basic block exactly once.
All types must be consistent, never mix i32 and i64 without explicit cast.
Output raw LLVM IR only, absolutely no markdown fences, no explanation."""

SEEDS = [
    "adds two i32 integers and returns the sum",
    "returns the maximum of two i32 values using a branch",
    "checks if an i32 is even, returns 1 if even 0 if odd using urem",
    "computes factorial of 5 using a loop with alloca store and load",
    "returns absolute value of an i32 using icmp and select",
    "multiplies two i32 values and returns the product",
    "subtracts b from a and returns the result",
    "returns 1 if input is greater than 100 else returns 0",
    "computes sum of 1 to 10 using a loop",
    "returns the minimum of two i32 values using icmp and select",
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


def clean_ir(text):
    lines = text.splitlines()
    start_index = 0

    for i, line in enumerate(lines):
        if line.lstrip().startswith("define"):
            start_index = i
            break
    else:
        return text.strip()

    cleaned_lines = lines[start_index:]
    depth = 0
    started_body = False
    result = []

    for line in cleaned_lines:
        result.append(line)

        for char in line:
            if char == "{":
                depth += 1
                started_body = True
            elif char == "}":
                if depth > 0:
                    depth -= 1

        if started_body and depth == 0:
            break

    return "\n".join(result).strip()


def generate_ir(seed):
    prompt = f"{SYSTEM_PROMPT}\n\nGenerate an LLVM IR program that {seed}."
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Generate an LLVM IR program that {seed}."},
        ],
        temperature=0.7,
    )
    text = response.choices[0].message.content or ""
    return clean_ir(strip_markdown(text))


if __name__ == "__main__":
    output_dir = os.path.join("testcases", "generated")
    os.makedirs(output_dir, exist_ok=True)

    total = len(SEEDS)

    for i, seed in enumerate(SEEDS):
        print(f"[{i + 1}/{total}] Generating: {seed}")
        try:
            ir = generate_ir(seed)
            output_path = os.path.join(output_dir, f"gen_{i}.ll")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(ir)

            preview = ir.splitlines()[0] if ir.splitlines() else ""
            print(preview)
        except Exception as exc:
            print(f"Error generating seed {i}: {seed}")
            print(exc)
