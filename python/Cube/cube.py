class Cube:

    def __init__(self,
            squares: list[int] = [i//9 for i in range(54)],
            centers: list[int] = [i for i in range(6)],
            moves:   list[str] = []
        ):
        self.squares = squares.copy()
        self.centers = centers.copy()
        self.moves = moves.copy()

    
    def spawn_child(self):
        return Cube(self.squares, self.centers, self.moves)

    
    def make_move(self, move: str, save=True):
        face, turns = move[0], int(move[1])

        moves = {
            'M': self._M, 'E': self._E, 'S': self._S,
            'F': self._F, 'f': self._f,
            'B': self._B, 'b': self._b,
            'L': self._L, 'l': self._l,
            'R': self._R, 'r': self._r,
            'U': self._U, 'u': self._u,
            'D': self._D, 'd': self._d
        }[face](turns)
        
        if save is False: return

        # Translate what face is being turned in code to what face the robot should turn
        # The two faces will differ if the cube in code was ever rotated

        str_to_int = {s: self.squares[i*9 + 4] for i, s in enumerate('BLURDF')}
        int_to_str = {self.centers[i]: s for i, s in enumerate('BLURDF')}
        
        for move in moves:
            face, turns = move[0], move[1]
            true_face = int_to_str[str_to_int[face]]
            self.moves.append(true_face + turns)


    def edge_solved(self, edge: int) -> bool:
        return self._current_edges()[edge] == self._solved_edges()[edge]


    def corner_solved(self, corner: int) -> bool:
        return self._current_corners()[corner] == self._solved_corners()[corner]
    

    def find_edge(self, edge: int) -> int:
        e1 = self._solved_edges()[edge]
        for i, e2 in enumerate(self._current_edges()):
            if set(e1) == set(e2): return i

    
    def find_corner(self, corner: int) -> int:
        c1 = self._solved_corners()[corner]
        for i, c2 in enumerate(self._current_corners()):
            if set(c1) == set(c2): return i


    def _current_edges(self) -> list[tuple[int]]:
        return [
            # Top layer
            (self.squares[46], self.squares[25]), # FU
            (self.squares[30], self.squares[23]), # RU
            (self.squares[ 7], self.squares[19]), # BU
            (self.squares[14], self.squares[21]), # LU

            # Middle layer
            (self.squares[48], self.squares[16]), # FL
            (self.squares[34], self.squares[50]), # RF
            (self.squares[ 5], self.squares[28]), # BR
            (self.squares[10], self.squares[ 3]), # LB

            # Bottom layer
            (self.squares[52], self.squares[43]), # FD
            (self.squares[32], self.squares[39]), # RD
            (self.squares[ 1], self.squares[37]), # BD
            (self.squares[12], self.squares[41])  # LD
        ]
    

    def _current_corners(self) -> list[tuple[int]]:
        return [
            # Top layer
            (self.squares[45], self.squares[17], self.squares[24]), # FLU
            (self.squares[33], self.squares[47], self.squares[26]), # RFU
            (self.squares[ 8], self.squares[27], self.squares[20]), # BRU
            (self.squares[11], self.squares[ 6], self.squares[18]), # LBU

            # Bottom layer
            (self.squares[51], self.squares[44], self.squares[15]), # FDL
            (self.squares[35], self.squares[42], self.squares[53]), # RDF
            (self.squares[ 2], self.squares[36], self.squares[29]), # BDR
            (self.squares[ 9], self.squares[38], self.squares[ 0])  # LDB
        ]
    

    def _solved_edges(self) -> list[tuple[int]]:
        b, l, u, r, d, f = 4, 13, 22, 31, 40, 49
        return [
            # Top layer
            (self.squares[f], self.squares[u]), # FU
            (self.squares[r], self.squares[u]), # RU
            (self.squares[b], self.squares[u]), # BU
            (self.squares[l], self.squares[u]), # LU

            # Middle layer
            (self.squares[f], self.squares[l]), # FL
            (self.squares[r], self.squares[f]), # RF
            (self.squares[b], self.squares[r]), # BR
            (self.squares[l], self.squares[b]), # LB

            # Bottom layer
            (self.squares[f], self.squares[d]), # FD
            (self.squares[r], self.squares[d]), # RD
            (self.squares[b], self.squares[d]), # BD
            (self.squares[l], self.squares[d])  # LD
        ]

    
    def _solved_corners(self) -> list[tuple[int]]:
        b, l, u, r, d, f = 4, 13, 22, 31, 40, 49
        return [
            # Top layer
            (self.squares[f], self.squares[l], self.squares[u]), # FLU
            (self.squares[r], self.squares[f], self.squares[u]), # RFU
            (self.squares[b], self.squares[r], self.squares[u]), # BRU
            (self.squares[l], self.squares[b], self.squares[u]), # LBU

            # Bottom layer
            (self.squares[f], self.squares[d], self.squares[l]), # FDL
            (self.squares[r], self.squares[d], self.squares[f]), # RDF
            (self.squares[b], self.squares[d], self.squares[r]), # BDR
            (self.squares[l], self.squares[d], self.squares[b])  # LDB
        ]
  

    def rotate_x_axis(self, n=1):
        self._R(n); self._M(4-n); self._L(4-n)

        
    def rotate_y_axis(self, n=1):
        self._U(n); self._E(4-n); self._D(4-n)

    
    def rotate_z_axis(self, n=1):
        self._F(n); self._S(n); self._B(4-n)

        
    def _M(self, n: int) -> tuple[str]:
        self._swap(n, [[1, 19, 46, 43], [4, 22, 49, 40], [7, 25, 52, 37]])
        return f'L{4-n}', f'R{n}'


    def _E(self, n: int) -> tuple[str]:
        self._swap(n, [[5, 10, 48, 34], [4, 13, 49, 31], [3, 16, 50, 28]])
        return f'D{4-n}', f'U{n}'


    def _S(self, n: int) -> tuple[str]:
        self._swap(n, [[12, 21, 30, 39], [13, 22, 31, 40], [14, 23, 32, 41]])
        return f'F{4-n}', f'B{n}'


    def _F(self, n: int) -> tuple[str]:
        self._swap(n, [
            [15, 24, 33, 42], [16, 25, 34, 43], [17, 26, 35, 44],
            [45, 47, 53, 51], [46, 50, 52, 48] # Rotate F face
        ])
        return f'F{n}',


    def _B(self, n: int) -> tuple[str]:
        self._swap(n, [
            [11, 38, 29, 20], [10, 37, 28, 19], [9, 36, 27, 18],
            [0, 2, 8, 6], [1, 5, 7, 3] # Rotate B face
        ])
        return f'B{n}',


    def _L(self, n: int) -> tuple[str]:
        self._swap(n, [
            [0, 18, 45, 44], [3, 21, 48, 41], [6, 24, 51, 38],
            [9, 11, 17, 15], [10, 14, 16, 12] # Rotate L face
        ])
        return f'L{n}',


    def _R(self, n: int) -> tuple[str]:
        self._swap(n, [
            [8, 36, 53, 26], [5, 39, 50, 23], [2, 42, 47, 20],
            [27, 29, 35, 33], [28, 32, 34, 30] # Rotate R face
        ])
        return f'R{n}',


    def _U(self, n: int) -> tuple[str]:
        self._swap(n, [
            [6, 27, 47, 17], [7, 30, 46, 14], [8, 33, 45, 11],
            [18, 20, 26, 24], [19, 23, 25, 21] # Rotate U face
        ])
        return f'U{n}',


    def _D(self, n: int) -> tuple[str]:
        self._swap(n, [
            [2, 9, 51, 35], [1, 12, 52, 32], [0, 15, 53, 29],
            [36, 38, 44, 42], [37, 41, 43, 39] # Rotate D face
        ])
        return f'D{n}',


    def _f(self, n: int) -> tuple[str]:
        self._F(n); self._S(n)
        return f'B{n}',


    def _b(self, n: int) -> tuple[str]:
        self._B(n); self._S(4-n)
        return f'F{n}',


    def _l(self, n: int) -> tuple[str]:
        self._L(n); self._M(n)
        return f'R{n}',


    def _r(self, n: int) -> tuple[str]:
        self._R(n); self._M(4-n)
        return f'L{n}',


    def _u(self, n: int) -> tuple[str]:
        self._U(n); self._E(4-n)
        return f'D{n}',


    def _d(self, n: int) -> tuple[str]:
        self._D(n); self._E(n)
        return f'U{n}',


    def _swap(self, n: int, swaps: list[list[int]]):
        for w, x, y, z in swaps:
            if   n == 1: a, b, c, d = z, w, x, y
            elif n == 2: a, b, c, d = y, z, w, x
            elif n == 3: a, b, c, d = x, y, z, w

            self.squares[w], self.squares[x], self.squares[y], self.squares[z] = \
            self.squares[a], self.squares[b], self.squares[c], self.squares[d]
