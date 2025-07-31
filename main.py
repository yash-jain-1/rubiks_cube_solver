from cube import Cube
from solver import solve_cube
from visualizer import display_cube

cube = Cube()
cube.scramble()
print("Scrambled Cube:")
display_cube(cube)

facelets = cube.to_facelet_string()
solution = solve_cube(facelets)

print("\nSolution:", solution)