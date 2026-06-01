cat > "/mnt/f/Engineering/Compiler Design/README.md" << 'EOF'
# 🔬 LLVM IR Test Lab
### Assignment 19 — LLM-Guided LLVM IR Test Generation for Differential Testing

A system that uses a Large Language Model to generate, validate, mutate, and differentially test LLVM IR programs to find compiler optimization bugs.

## What It Does
1. **Generate** — LLM generates LLVM IR from plain English descriptions
2. **Validate** — `opt -passes=verify` + custom SSA, PHI, type, terminator checks
3. **Mutate** — LLM applies 4 mutation types to valid IR
4. **Repair** — LLM attempts to fix invalid IR using error feedback
5. **Diff Test** — Compiles at -O0, -O2, -O3 and compares outputs

## Results
| Metric | Value |
|--------|-------|
| IR Generation Validity Rate | 70% |
| Mutation Validity Rate | 100% |
| Repair Success Rate | 33% |
| Differential Test Divergences | 0 |

## Setup
```bash
git clone <your-repo>
cd "Compiler Design"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key"
python3 app.py
```
Open `http://localhost:5000` in your browser.

## Tech Stack
- **LLM:** Groq API (llama-3.3-70b-versatile)
- **Compiler Tools:** LLVM opt, clang
- **Web UI:** Flask + vanilla JS
- **Language:** Python 3.12
EOF