import random

COLORS = {
    'U': 'W', 'D': 'Y',
    'F': 'G', 'B': 'B',
    'L': 'O', 'R': 'R'
}

MOVES = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"]

class Cube:
    def __init__(self):
        self.faces = {face: [[COLORS[face]]*3 for _ in range(3)] for face in COLORS}

    def rotate_face(self, face):
        self.faces[face] = [list(reversed(col)) for col in zip(*self.faces[face])]

    def rotate_face_ccw(self, face):
        self.faces[face] = list(zip(*self.faces[face]))[::-1]
        self.faces[face] = [list(row) for row in self.faces[face]]

    def move(self, notation):
        # Only implements U/U' and D/D' for brevity
        if notation == 'U':
            self.rotate_face('U')
            self._cycle(['F', 'R', 'B', 'L'], row=0)
        elif notation == "U'":
            self.rotate_face_ccw('U')
            self._cycle(['F', 'L', 'B', 'R'], row=0)
        elif notation == 'D':
            self.rotate_face('D')
            self._cycle(['F', 'L', 'B', 'R'], row=2)
        elif notation == "D'":
            self.rotate_face_ccw('D')
            self._cycle(['F', 'R', 'B', 'L'], row=2)
        # Add R, L, F, B moves here

    def _cycle(self, sides, row):
        temp = self.faces[sides[0]][row][:]
        for i in range(3):
            self.faces[sides[i]][row] = self.faces[sides[i+1]][row]
        self.faces[sides[3]][row] = temp

    def scramble(self, n=20):
        return [self.move(random.choice(MOVES)) for _ in range(n)]

    def to_facelet_string(self):
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        return ''.join(self.faces[face][i][j] for face in order for i in range(3) for j in range(3))

    def print_net(self):
        for face in self.faces:
            print(f"{face}:")
            for row in self.faces[face]:
                print(' '.join(row))
            print()
