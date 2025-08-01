def display_cube(cube):
    cube.print_net()


def visualize_solution(cube, solution):
    print("Solution steps:")
    for step in solution:
        print(step)
    cube.print_net()
    display_cube(cube)