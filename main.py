from cube import Cube
from solver import solve_cube, bfs_solver, astar_solver
from visualizer import display_cube

cube = Cube()
scramble_seq = cube.scramble()
print("Scrambled Cube:", scramble_seq)
display_cube(cube)

facelets = cube.to_facelet_string()
kociemba_solution = solve_cube(facelets)
print("\nKociemba Solution:", kociemba_solution)

bfs_solution = bfs_solver(cube.clone())
print("BFS Solution:", bfs_solution)

astar_solution = astar_solver(cube.clone())
print("A* Solution:", astar_solution)