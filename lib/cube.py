import random
import copy

COLORS = {
    'U': 'W', 'D': 'Y',
    'F': 'G', 'B': 'B',
    'L': 'O', 'R': 'R'
}

MOVES = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"]

class Cube:
    def __init__(self):
        self.faces = {face: [[COLORS[face]]*3 for _ in range(3)] for face in COLORS}

    def clone(self):
        clone = Cube()
        clone.faces = copy.deepcopy(self.faces)
        return clone

    def rotate_face(self, face):
        self.faces[face] = [list(reversed(col)) for col in zip(*self.faces[face])]

    def rotate_face_ccw(self, face):
        self.faces[face] = list(zip(*self.faces[face]))[::-1]
        self.faces[face] = [list(row) for row in self.faces[face]]

    def move(self, notation):
        rotate_adj = {
            'U': (['F', 'R', 'B', 'L'], 0),
            "U'": (['F', 'L', 'B', 'R'], 0),
            'D': (['F', 'L', 'B', 'R'], 2),
            "D'": (['F', 'R', 'B', 'L'], 2),
            'R': self._move_r,
            "R'": self._move_r_prime,
            'L': self._move_l,
            "L'": self._move_l_prime,
            'F': self._move_f,
            "F'": self._move_f_prime,
            'B': self._move_b,
            "B'": self._move_b_prime
        }
        if notation in ['U', "U'", 'D', "D'"]:
            face = notation[0]
            if "'" in notation:
                self.rotate_face_ccw(face)
            else:
                self.rotate_face(face)
            sides, row = rotate_adj[notation]
            self._cycle(sides, row=row)
        else:
            rotate_adj[notation]()

    def _cycle(self, sides, row):
        temp = self.faces[sides[0]][row][:]
        for i in range(3):
            self.faces[sides[i]][row] = self.faces[sides[i+1]][row]
        self.faces[sides[3]][row] = temp

    def _move_r(self):
        self.rotate_face('R')
        for i in range(3):
            self.faces['U'][i][2], self.faces['F'][i][2], self.faces['D'][i][2], self.faces['B'][2 - i][0] = \
                self.faces['B'][2 - i][0], self.faces['U'][i][2], self.faces['F'][i][2], self.faces['D'][i][2]

    def _move_r_prime(self):
        self.rotate_face_ccw('R')
        for i in range(3):
            self.faces['U'][i][2], self.faces['B'][2 - i][0], self.faces['D'][i][2], self.faces['F'][i][2] = \
                self.faces['F'][i][2], self.faces['U'][i][2], self.faces['B'][2 - i][0], self.faces['D'][i][2]

    def _move_l(self):
        self.rotate_face('L')
        for i in range(3):
            self.faces['U'][i][0], self.faces['B'][2 - i][2], self.faces['D'][i][0], self.faces['F'][i][0] = \
                self.faces['F'][i][0], self.faces['U'][i][0], self.faces['B'][2 - i][2], self.faces['D'][i][0]

    def _move_l_prime(self):
        self.rotate_face_ccw('L')
        for i in range(3):
            self.faces['U'][i][0], self.faces['F'][i][0], self.faces['D'][i][0], self.faces['B'][2 - i][2] = \
                self.faces['B'][2 - i][2], self.faces['U'][i][0], self.faces['F'][i][0], self.faces['D'][i][0]

    def _move_f(self):
        self.rotate_face('F')
        for i in range(3):
            self.faces['U'][2][i], self.faces['R'][i][0], self.faces['D'][0][2 - i], self.faces['L'][2 - i][2] = \
                self.faces['L'][2 - i][2], self.faces['U'][2][i], self.faces['R'][i][0], self.faces['D'][0][2 - i]

    def _move_f_prime(self):
        self.rotate_face_ccw('F')
        for i in range(3):
            self.faces['U'][2][i], self.faces['L'][2 - i][2], self.faces['D'][0][2 - i], self.faces['R'][i][0] = \
                self.faces['R'][i][0], self.faces['U'][2][i], self.faces['L'][2 - i][2], self.faces['D'][0][2 - i]

    def _move_b(self):
        self.rotate_face('B')
        for i in range(3):
            self.faces['U'][0][i], self.faces['L'][2 - i][0], self.faces['D'][2][2 - i], self.faces['R'][i][2] = \
                self.faces['R'][i][2], self.faces['U'][0][i], self.faces['L'][2 - i][0], self.faces['D'][2][2 - i]

    def _move_b_prime(self):
        self.rotate_face_ccw('B')
        for i in range(3):
            self.faces['U'][0][i], self.faces['R'][i][2], self.faces['D'][2][2 - i], self.faces['L'][2 - i][0] = \
                self.faces['L'][2 - i][0], self.faces['U'][0][i], self.faces['R'][i][2], self.faces['D'][2][2 - i]

    def scramble(self, n=20):
        scramble_seq = [random.choice(MOVES) for _ in range(n)]
        for move in scramble_seq:
            self.move(move)
        return scramble_seq

    def to_facelet_string(self):
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        return ''.join(self.faces[face][i][j] for face in order for i in range(3) for j in range(3))

    def print_net(self):
        for face in self.faces:
            print(f"{face}:")
            for row in self.faces[face]:
                print(' '.join(row))
            print()