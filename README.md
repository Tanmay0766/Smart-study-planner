# Smart Study Planner

A mini Python project that recommends a study plan based on energy level, time available, and task complexity using fuzzy logic.

## Features

- Fuzzy membership functions for energy, time, and complexity
- Rule-based inference to recommend study session length, focus intensity, and rest time
- Simple CLI example to generate a personalized study plan

## Getting Started

### Requirements

- Python 3.8+

### Run

```bash
python study_planner.py
```

### Frontend

Open `frontend/index.html` in your browser to use the interactive study planner with a polished UI.

### Run frontend locally

From `d:\smart study`:

```powershell
cd "d:\smart study"
python serve.py
```

Then open:

```text
http://localhost:8000
```

This serves the app from `frontend/index.html` and makes the UI available through localhost.

### Example

Enter your current energy level, time available, and task complexity. The planner uses fuzzy logic to suggest:

- study session length
- focus intensity
- rest recommendation

## Files

- `study_planner.py`: main planner and CLI
- `test_study_planner.py`: unit tests for the fuzzy planner
