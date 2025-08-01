from lib.cube import Cube
from lib.solver import solve_cube, bfs_solver, astar_solver
from lib.visualizer import display_cube
from collections import Counter
import sys

cube = Cube()
scramble_seq = cube.scramble()
print("="*40)
print("Scrambled Cube Moves:")
print(' '.join(scramble_seq))
print("="*40)
display_cube(cube)

facelets = cube.to_facelet_string()
print("="*40)
print("Facelet string:", facelets)
print("Length:", len(facelets))
print("Counts:", Counter(facelets))
print("="*40)
try:
    kociemba_solution = solve_cube(facelets)
    print("Kociemba Solution:", kociemba_solution)
except Exception as e:
    print("Kociemba solver error:", e)
    sys.exit(1)

print("="*40)
# Only run BFS/A* if scramble is short
if len(scramble_seq) <= 4:
    bfs_solution = bfs_solver(cube.clone(), max_depth=7)
    print("BFS Solution:", bfs_solution if bfs_solution else "No solution found within depth limit.")
    astar_solution = astar_solver(cube.clone(), max_depth=10)
    print("A* Solution:", astar_solution if astar_solution else "No solution found within depth limit.")
else:
    print("WARNING: BFS and A* solvers are too slow for real scrambles. Try with a simpler scramble (<=4 moves).")
    sys.exit(0)