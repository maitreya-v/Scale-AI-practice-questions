# Day 1 Debugging Practical — Project Assignment Pipeline

**Fidelity:** High-confidence reconstruction

**Time limit:** 60 minutes

## Scenario

You have joined a team that maintains a small internal system for assigning contributors to projects. The repository contains several files and a small dataset describing contributors, courses, and projects.

Projects have priorities and capacities. Some projects require contributors to have completed particular courses. The public API and test names are already used by downstream code, so **do not change function signatures or test expectations**.

The codebase currently contains **six logical bugs**. Your goal is to identify and fix all six while preserving the public API.

## What to do

From this directory:

```bash
pytest -q
```

Then debug the failing behavior. You may add temporary logging/print statements while working, but remove noisy instrumentation when finished.

## Interview-style constraints

- Do not rewrite the project from scratch.
- Preserve existing function/class names and signatures.
- Prefer small, targeted fixes.
- Use the tests to drive investigation.
- Assume the data files are valid unless a test suggests otherwise.
- Explain your hypothesis before each meaningful change.

## Publicly reported structure mirrored here

The reconstruction includes three test themes publicly reported for a Scale debugging round:

1. Assign contributors to projects that have no course requirements.
2. Assign contributors only when required courses were completed.
3. Determine the course required by the greatest number of projects.

Four bug categories were publicly described in candidate reports. Two additional bugs affecting the third theme were not publicly disclosed, so this practice version supplies original replacements that exercise the same debugging skills.

## Practice setup

Use Python 3.10 or newer. This branch contains only this exercise from the
prepared practice pack. The starter code, datasets, and tests are unchanged.

```bash
git clone --single-branch --branch debugging-project-assignment https://github.com/maitreya-v/Scale-AI-practice-questions.git
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
