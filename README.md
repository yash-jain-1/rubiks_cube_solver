# Rubik's Cube Solver

This project models and solves a Rubik's Cube using real-world move logic and multiple solving strategies.

## Features
- Full 3x3 cube move engine with all 12 face turns
- Scrambler
- Solver using:
  - Kociemba’s optimal algorithm (via `kociemba` lib)
  - BFS (bounded-depth)
  - A* Search with heuristic (misplaced tiles)
- Visual output in CLI

## How to Run
```bash
pip install -r requirements.txt
python main.py
```


## Coming Soon
- 2D/3D visualizer
- Beginner method solver