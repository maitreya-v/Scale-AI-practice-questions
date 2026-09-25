# Day 1 Debugging Practical — Silent LLM Output

**Fidelity:** Reported variant

**Time limit:** 60 minutes

## Scenario

A small application calls a hosted language model, but the end-to-end pipeline returns no useful output for valid requests. The code is modular and the failure is not localized to one obvious line.

Your task is to trace the request through the pipeline, isolate the defects, and make the existing tests pass without changing the public API.

Public interview guides report a Scale debugging variant involving a roughly 150–200 line code path, several coupled methods, a model endpoint, and prompt-hashing/caching logic. This reconstruction uses a deterministic fake model so you can practice without an API key.

## Run

```bash
pytest -q
```

## Constraints

- Do not replace the architecture wholesale.
- Preserve public method/function signatures.
- Use targeted instrumentation to identify where valid data turns into invalid or empty data.
- There are **three logical defects** in the starter code.

## Practice setup

Use Python 3.10 or newer. This branch contains only this exercise from the
prepared practice pack. The starter code, datasets, and tests are unchanged.

```bash
git clone --single-branch --branch debugging-llm-silent-output https://github.com/maitreya-v/Scale-AI-practice-questions.git
cd Scale-AI-practice-questions
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

On Windows, activate the environment with `.venv\Scripts\activate`.
Run commands from the repository root. Failing tests are expected until you
complete the exercise; there is no answer key in this branch.

This is an original practice reconstruction based on public interview reports
and guides, not an official Scale AI repository or proprietary interview material.
