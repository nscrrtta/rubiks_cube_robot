# Moves
F = "F1";    F2 = "F2";    Fi = "F3"
B = "B1";    B2 = "B2";    Bi = "B3"
L = "L1";    L2 = "L2";    Li = "L3"
R = "R1";    R2 = "R2";    Ri = "R3"
U = "U1";    U2 = "U2";    Ui = "U3"
D = "D1";    D2 = "D2";    Di = "D3"
M = "M1";    M2 = "M2";    Mi = "M3"
E = "E1";    E2 = "E2";    Ei = "E3"
S = "S1";    S2 = "S2";    Si = "S3"

f = "f1";    f2 = "f2";    fi = "f3"
b = "b1";    b2 = "b2";    bi = "b3"
l = "l1";    l2 = "l2";    li = "l3"
r = "r1";    r2 = "r2";    ri = "r3"
u = "u1";    u2 = "u2";    ui = "u3"
d = "d1";    d2 = "d2";    di = "d3"


"""
Tune these variables to adjust speed vs number of moves

Higher values:
  - Explore more options
  - Code will take longer
  - Solution will have fewer moves

Lower values:
  - Explore less options
  - Code will be faster
  - Solution will have more moves
"""

# Max number of cubes to solve cross
MAX_SOLVE_CROSS = 200

# First number: How many cubes with cross solved to continue solving
# Second number: How many of those cubes should contain U moves
NUM_CUBES_CROSS = (10, 3)

# Max number of cubes to solve F2L (per cube with cross solved)
MAX_SOLVE_F2L = 50

# How many cubes with F2L solved to continue solving
NUM_CUBES_F2L = 100
