# Rubik's Cube Solver

This project models and solves a Rubik's Cube using real-world move logic and multiple solving strategies. It includes both a command-line interface (CLI) and a frontend visualizer.

## Features
- Full 3x3 cube move engine with all 12 face turns
- Scrambler
- Solver using:
  - Kociemba’s optimal algorithm (via `kociemba` lib)
  - BFS (bounded-depth)
  - A* Search with heuristic (misplaced tiles)
- Visual output in CLI
- **Frontend visualizer** for interactive cube manipulation and solution display

## How to Run (CLI)

You can use the Makefile for setup and running:

```bash
make run
```

Or manually:

```bash
pip install -r requirements.txt
python main.py
```

## How to Run the Frontend Visualizer

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2. Install frontend dependencies:
    ```bash
    npm install
    ```
3. Start the frontend development server:
    ```bash
    npm start
    ```
4. Open your browser and go to [http://localhost:3000](http://localhost:3000) (or the port shown in your terminal).

## Project Structure

- `main.py` — CLI entry point
- `lib/` — Cube logic, solvers, and CLI visualizer
- `frontend/` — Frontend visualizer (React or similar)
- `tests/` — Unit tests

---
