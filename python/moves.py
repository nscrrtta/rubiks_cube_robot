from constants import *
"""
                Back
                |  0  1  2 |
                |  3  4  5 |
                |  6  7  8 |

Left            Up              Right           Down
|  9 10 11 |    | 18 19 20 |    | 27 28 29 |    | 36 37 38 |
| 12 13 14 |    | 21 22 23 |    | 30 31 32 |    | 39 40 41 |
| 15 16 17 |    | 24 25 26 |    | 33 34 35 |    | 42 43 44 |

                Front
                | 45 46 47 |
                | 48 49 50 |
                | 51 52 53 |
"""


class Moves:

    def turn_face(self, sqrs:list[int], move:str) -> tuple[str]:
        m, n = move[0], move[1]

        return {
        'M': self.M, 'E': self.E, 'S': self.S,
        'F': self.F, 'f': self.f,
        'B': self.B, 'b': self.b,
        'L': self.L, 'l': self.l,
        'R': self.R, 'r': self.r,
        'U': self.U, 'u': self.u,
        'D': self.D, 'd': self.d
        }[m](sqrs, int(n))


    def M(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[1],sqrs[19],sqrs[46],sqrs[43]=sqrs[43],sqrs[1],sqrs[19],sqrs[46]
            sqrs[4],sqrs[22],sqrs[49],sqrs[40]=sqrs[40],sqrs[4],sqrs[22],sqrs[49]
            sqrs[7],sqrs[25],sqrs[52],sqrs[37]=sqrs[37],sqrs[7],sqrs[25],sqrs[52]
        return f'L{4-n}', f'R{n}'


    def E(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[5],sqrs[10],sqrs[48],sqrs[34]=sqrs[34],sqrs[5],sqrs[10],sqrs[48]
            sqrs[4],sqrs[13],sqrs[49],sqrs[31]=sqrs[31],sqrs[4],sqrs[13],sqrs[49]
            sqrs[3],sqrs[16],sqrs[50],sqrs[28]=sqrs[28],sqrs[3],sqrs[16],sqrs[50]
        return f'D{4-n}', f'U{n}'


    def S(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[12],sqrs[21],sqrs[30],sqrs[39]=sqrs[39],sqrs[12],sqrs[21],sqrs[30]
            sqrs[13],sqrs[22],sqrs[31],sqrs[40]=sqrs[40],sqrs[13],sqrs[22],sqrs[31]
            sqrs[14],sqrs[23],sqrs[32],sqrs[41]=sqrs[41],sqrs[14],sqrs[23],sqrs[32]
        return f'F{4-n}', f'B{n}'


    def F(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[15],sqrs[24],sqrs[33],sqrs[42]=sqrs[42],sqrs[15],sqrs[24],sqrs[33]
            sqrs[16],sqrs[25],sqrs[34],sqrs[43]=sqrs[43],sqrs[16],sqrs[25],sqrs[34]
            sqrs[17],sqrs[26],sqrs[35],sqrs[44]=sqrs[44],sqrs[17],sqrs[26],sqrs[35]
            self.rotate_face(sqrs, 45)
        return f'F{n}',


    def f(self, sqrs:list[int], n:int)-> tuple[str]:
        self.F(sqrs, n)
        self.S(sqrs, n)
        return f'B{n}',


    def B(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[11],sqrs[38],sqrs[29],sqrs[20]=sqrs[20],sqrs[11],sqrs[38],sqrs[29]
            sqrs[10],sqrs[37],sqrs[28],sqrs[19]=sqrs[19],sqrs[10],sqrs[37],sqrs[28]
            sqrs[9], sqrs[36],sqrs[27],sqrs[18]=sqrs[18],sqrs[9], sqrs[36],sqrs[27]
            self.rotate_face(sqrs, 0)
        return f'B{n}',


    def b(self, sqrs:list[int], n:int)-> tuple[str]:
        self.B(sqrs, n)
        self.S(sqrs, 4-n)
        return f'F{n}',


    def L(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[0],sqrs[18],sqrs[45],sqrs[44]=sqrs[44],sqrs[0],sqrs[18],sqrs[45]
            sqrs[3],sqrs[21],sqrs[48],sqrs[41]=sqrs[41],sqrs[3],sqrs[21],sqrs[48]
            sqrs[6],sqrs[24],sqrs[51],sqrs[38]=sqrs[38],sqrs[6],sqrs[24],sqrs[51]
            self.rotate_face(sqrs, 9)
        return f'L{n}',


    def l(self, sqrs:list[int], n:int)-> tuple[str]:
        self.L(sqrs, n)
        self.M(sqrs, n)
        return f'R{n}',


    def R(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[8],sqrs[36],sqrs[53],sqrs[26]=sqrs[26],sqrs[8],sqrs[36],sqrs[53]
            sqrs[5],sqrs[39],sqrs[50],sqrs[23]=sqrs[23],sqrs[5],sqrs[39],sqrs[50]
            sqrs[2],sqrs[42],sqrs[47],sqrs[20]=sqrs[20],sqrs[2],sqrs[42],sqrs[47]
            self.rotate_face(sqrs, 27)
        return f'R{n}',


    def r(self, sqrs:list[int], n:int)-> tuple[str]:
        self.R(sqrs, n)
        self.M(sqrs, 4-n)
        return f'L{n}',


    def U(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[6],sqrs[27],sqrs[47],sqrs[17]=sqrs[17],sqrs[6],sqrs[27],sqrs[47]
            sqrs[7],sqrs[30],sqrs[46],sqrs[14]=sqrs[14],sqrs[7],sqrs[30],sqrs[46]
            sqrs[8],sqrs[33],sqrs[45],sqrs[11]=sqrs[11],sqrs[8],sqrs[33],sqrs[45]
            self.rotate_face(sqrs, 18)
        return f'U{n}',


    def u(self, sqrs:list[int], n:int)-> tuple[str]:
        self.U(sqrs, n)
        self.E(sqrs, 4-n)
        return f'D{n}',


    def D(self, sqrs:list[int], n:int)-> tuple[str]:
        for _ in range(n):
            sqrs[2],sqrs[9], sqrs[51],sqrs[35]=sqrs[35],sqrs[2],sqrs[9], sqrs[51]
            sqrs[1],sqrs[12],sqrs[52],sqrs[32]=sqrs[32],sqrs[1],sqrs[12],sqrs[52]
            sqrs[0],sqrs[15],sqrs[53],sqrs[29]=sqrs[29],sqrs[0],sqrs[15],sqrs[53]
            self.rotate_face(sqrs, 36)
        return f'D{n}',


    def d(self, sqrs:list[int], n:int)-> tuple[str]:
        self.D(sqrs, n)
        self.E(sqrs, n)
        return f'U{n}',


    def rotate_face(self, sqrs:list[int], i:int):
        # Create 3x3 matrix
        m = [sqrs[i + j*3 : i + (j+1)*3] for j in range(3)]
        # Rotate matrix clockwise
        m = list(zip(*m[::-1]))
        # Create list and put it in sqrs
        sqrs[i:i+9] = m[0]+m[1]+m[2]


    def rotate_cube(self, sqrs:list[int], axis:str):
        # Create 6x9 matrix
        m = [sqrs[i*9:(i+1)*9] for i in range(6)]

        # Swap faces
        if axis == x:
            m[0],m[2],m[4],m[5] = m[2],m[5],m[0],m[4]
            rotations = [0, 3, 0, 1, 2, 2]
        elif axis == xi:
            m[0],m[2],m[4],m[5] = m[4],m[0],m[5],m[2]
            rotations = [2, 1, 0, 3, 2, 0]
        elif axis == y:
            m[0],m[1],m[3],m[5] = m[1],m[5],m[0],m[3]
            rotations = [1, 1, 1, 1, 3, 1]
        elif axis == yi:
            m[0],m[1],m[3],m[5] = m[3],m[0],m[5],m[1]
            rotations = [3, 3, 3, 3, 1, 3]
        elif axis == z:
            m[1],m[2],m[3],m[4] = m[4],m[1],m[2],m[3]
            rotations = [3, 0, 0, 0, 0, 1]
        elif axis == zi:
            m[1],m[2],m[3],m[4] = m[2],m[3],m[4],m[1]
            rotations = [1, 0, 0, 0, 0, 3]

        # Create list
        sqrs[:] = m[0]+m[1]+m[2]+m[3]+m[4]+m[5]

        # Rotate faces
        for i, n in enumerate(rotations):
            for _ in range(n): self.rotate_face(sqrs, i*9)
