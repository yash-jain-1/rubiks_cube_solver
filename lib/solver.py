import kociemba
# The . tells Python to look in the same package directory (lib/).
from .cube import Cube, MOVES
from collections import deque
import heapq


def solve_cube(facelet_string):
    return kociemba.solve(facelet_string)


def heuristic(cube):
    solved = Cube()
    return sum(cube.faces[f][i][j] != solved.faces[f][i][j] for f in cube.faces for i in range(3) for j in range(3))


def bfs_solver(start_cube, max_depth=7):
    visited = set()
    queue = deque([(start_cube, [])])

    while queue:
        current, path = queue.popleft()
        key = current.to_facelet_string()
        if key in visited:
            continue
        visited.add(key)
        if heuristic(current) == 0:
            return path
        if len(path) >= max_depth:
            continue
        for move in MOVES:
            new_cube = current.clone()
            new_cube.move(move)
            queue.append((new_cube, path + [move]))
    return None


def astar_solver(start_cube, max_depth=10):
    visited = set()
    heap = [(heuristic(start_cube), 0, start_cube, [])]

    while heap:
        _, cost, current, path = heapq.heappop(heap)
        key = current.to_facelet_string()
        if key in visited:
            continue
        visited.add(key)
        if heuristic(current) == 0:
            return path
        if len(path) >= max_depth:
            continue
        for move in MOVES:
            new_cube = current.clone()
            new_cube.move(move)
            heapq.heappush(heap, (heuristic(new_cube) + cost + 1, cost + 1, new_cube, path + [move]))
    return None

