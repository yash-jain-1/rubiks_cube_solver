import pytest
from lib.cube import Cube, MOVES

def test_solved_cube_facelet_string():
    cube = Cube()
    facelets = cube.to_facelet_string()
    # Solved cube should have 9 of each face letter in order
    assert len(facelets) == 54
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        assert facelets.count(face) == 9

def test_move_and_inverse():
    cube = Cube()
    for move in MOVES:
        cube2 = cube.clone()
        cube2.move(move)
        # Apply the inverse move
        if "'" in move:
            inverse = move.replace("'", "")
        else:
            inverse = move + "'"
        cube2.move(inverse)
        # After move and its inverse, should be solved
        assert cube2.to_facelet_string() == cube.to_facelet_string()

def test_scramble_length():
    cube = Cube()
    scramble = cube.scramble(n=10)
    assert len(scramble) == 10

def test_clone_independence():
    cube1 = Cube()
    cube2 = cube1.clone()
    cube2.move("R")
    assert cube1.to_facelet_string() !