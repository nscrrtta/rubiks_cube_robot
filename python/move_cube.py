from constants import x, xi, y, yi, z, zi
"""
This script contains all the functions that move the cube in code
by changing the list <sqrs>, which is a 1D list of 54 integers 0 to 5 (inclusive)
representing the current state of the cube

The diagram below shows a 2D layout of the cube and the indices of <sqrs>

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

def rotate_face(sqrs: list, n: int, top_left: int):
    """
    This function rotates the 9 squares within a face

    <n> is the number of clockwise rotations

    <top_left> is the top-left integer of the face to be rotated:
        0:  back
        9:  left
        18: up
        27: right
        36: down
        45: front

    Note: each pass of the for loop below does half of a clockwise rotation
    """

    for _ in range( n*2 ):
        temp = sqrs[top_left]
        for key, val in {0:3, 3:6, 6:7, 7:8, 8:5, 5:2, 2:1}.items():
            sqrs[top_left+key] = sqrs[top_left+val]
        sqrs[top_left+val] = temp

def rotate_cube(sqrs: list, rotation: str):
    """
    This function rotates the entire cube

    <rotation> is a string representing the axis of rotation (see constants.py)

    <face_shifts> is a dictionary representing where faces are shifted to
    <face_rotations> is a list representing the number of times each face is rotated

    For example, if <rotation> is "z":

        face shifts:

            face 2 becomes face 1 (up    becomes left )
            face 1 becomes face 4 (left  becomes down )
            face 4 becomes face 3 (down  becomes right)
            face 3 becomes face 2 (right becomes up   )

        face rotations:

            face 0 (front) is rotate counter-clockwise once
            face 5 (back)  is rotate clockwise once
    """

    face_shifts, face_rotations = {
        x: ({0:2, 2:5, 5:4}, [0, 3, 0, 1, 2, 2]),
        xi:({0:4, 4:5, 5:2}, [2, 1, 0, 3, 2, 0]),
        y: ({5:3, 3:0, 0:1}, [1, 1, 1, 1, 3, 1]),
        yi:({5:1, 1:0, 0:3}, [3, 3, 3, 3, 1, 3]),
        z: ({2:1, 1:4, 4:3}, [3, 0, 0, 0, 0, 1]),
        zi:({2:3, 3:4, 4:1}, [1, 0, 0, 0, 0, 3])
    }[rotation]

    # Shift faces
    temp = list(face_shifts)[0]*9
    temp = sqrs[temp:temp+9]

    for key, val in face_shifts.items():
        for i in range(9): sqrs[key*9+i] = sqrs[val*9+i]
        
    for i in range(9): sqrs[val*9+i] = temp[i]

    # Rotate faces
    for f, n in enumerate(face_rotations):
        if n > 0: rotate_face(sqrs, n, top_left=f*9)

def M(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[1],sqrs[19],sqrs[46],sqrs[43]=sqrs[43],sqrs[1],sqrs[19],sqrs[46]
        sqrs[4],sqrs[22],sqrs[49],sqrs[40]=sqrs[40],sqrs[4],sqrs[22],sqrs[49]
        sqrs[7],sqrs[25],sqrs[52],sqrs[37]=sqrs[37],sqrs[7],sqrs[25],sqrs[52]

    return f'L{4-n}', f'R{n}'

def E(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[5],sqrs[10],sqrs[48],sqrs[34]=sqrs[34],sqrs[5],sqrs[10],sqrs[48]
        sqrs[4],sqrs[13],sqrs[49],sqrs[31]=sqrs[31],sqrs[4],sqrs[13],sqrs[49]
        sqrs[3],sqrs[16],sqrs[50],sqrs[28]=sqrs[28],sqrs[3],sqrs[16],sqrs[50]

    return f'D{4-n}', f'U{n}'

def S(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[12],sqrs[21],sqrs[30],sqrs[39]=sqrs[39],sqrs[12],sqrs[21],sqrs[30]
        sqrs[13],sqrs[22],sqrs[31],sqrs[40]=sqrs[40],sqrs[13],sqrs[22],sqrs[31]
        sqrs[14],sqrs[23],sqrs[32],sqrs[41]=sqrs[41],sqrs[14],sqrs[23],sqrs[32]

    return f'F{4-n}', f'B{n}'

def F(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[15],sqrs[24],sqrs[33],sqrs[42]=sqrs[42],sqrs[15],sqrs[24],sqrs[33]
        sqrs[16],sqrs[25],sqrs[34],sqrs[43]=sqrs[43],sqrs[16],sqrs[25],sqrs[34]
        sqrs[17],sqrs[26],sqrs[35],sqrs[44]=sqrs[44],sqrs[17],sqrs[26],sqrs[35]
    
    rotate_face(sqrs, n, top_left=45)

    return f'F{n}',

def f(sqrs: list, n: int) -> tuple:

    F(sqrs, n)
    S(sqrs, n)

    return f'B{n}',

def B(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[11],sqrs[38],sqrs[29],sqrs[20]=sqrs[20],sqrs[11],sqrs[38],sqrs[29]
        sqrs[10],sqrs[37],sqrs[28],sqrs[19]=sqrs[19],sqrs[10],sqrs[37],sqrs[28]
        sqrs[9], sqrs[36],sqrs[27],sqrs[18]=sqrs[18],sqrs[9], sqrs[36],sqrs[27]

    rotate_face(sqrs, n, top_left=0)

    return f'B{n}',

def b(sqrs: list, n: int) -> tuple:

    B(sqrs, n)
    S(sqrs, 4-n)

    return f'F{n}',

def L(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[0],sqrs[18],sqrs[45],sqrs[44]=sqrs[44],sqrs[0],sqrs[18],sqrs[45]
        sqrs[3],sqrs[21],sqrs[48],sqrs[41]=sqrs[41],sqrs[3],sqrs[21],sqrs[48]
        sqrs[6],sqrs[24],sqrs[51],sqrs[38]=sqrs[38],sqrs[6],sqrs[24],sqrs[51]

    rotate_face(sqrs, n, top_left=9)

    return f'L{n}',

def l(sqrs: list, n: int) -> tuple:

    L(sqrs, n)
    M(sqrs, n)

    return f'R{n}',

def R(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[8],sqrs[36],sqrs[53],sqrs[26]=sqrs[26],sqrs[8],sqrs[36],sqrs[53]
        sqrs[5],sqrs[39],sqrs[50],sqrs[23]=sqrs[23],sqrs[5],sqrs[39],sqrs[50]
        sqrs[2],sqrs[42],sqrs[47],sqrs[20]=sqrs[20],sqrs[2],sqrs[42],sqrs[47]

    rotate_face(sqrs, n, top_left=27)

    return f'R{n}',

def r(sqrs: list, n: int) -> tuple:

    R(sqrs, n)
    M(sqrs, 4-n)

    return f'L{n}',

def U(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[6],sqrs[27],sqrs[47],sqrs[17]=sqrs[17],sqrs[6],sqrs[27],sqrs[47]
        sqrs[7],sqrs[30],sqrs[46],sqrs[14]=sqrs[14],sqrs[7],sqrs[30],sqrs[46]
        sqrs[8],sqrs[33],sqrs[45],sqrs[11]=sqrs[11],sqrs[8],sqrs[33],sqrs[45]

    rotate_face(sqrs, n, top_left=18)

    return f'U{n}',

def u(sqrs: list, n: int) -> tuple:

    U(sqrs, n)
    E(sqrs, 4-n)

    return f'D{n}',

def D(sqrs: list, n: int) -> tuple:

    for _ in range(n):
        sqrs[2],sqrs[9], sqrs[51],sqrs[35]=sqrs[35],sqrs[2],sqrs[9], sqrs[51]
        sqrs[1],sqrs[12],sqrs[52],sqrs[32]=sqrs[32],sqrs[1],sqrs[12],sqrs[52]
        sqrs[0],sqrs[15],sqrs[53],sqrs[29]=sqrs[29],sqrs[0],sqrs[15],sqrs[53]

    rotate_face(sqrs, n, top_left=36)

    return f'D{n}',

def d(sqrs: list, n: int) -> tuple:

    D(sqrs, n)
    E(sqrs, n)

    return f'U{n}',
