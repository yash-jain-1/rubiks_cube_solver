def display_cube(cube):
    print("Cube State:")
    cube.print_net()

def visualize_solution(cube, solution):
    print("Solution steps:")
    for step in solution:
        print(step)
    print("Cube after solution:")
    display_cube(cube)