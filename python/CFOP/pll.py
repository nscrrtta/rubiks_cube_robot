from Cube.constants import *
from Cube.cube import Cube


class PLL:

    def solve_pll(self, cubes: list[Cube]):
        for cube in cubes: self._solve_pll(cube)


    def _solve_pll(self, cube: Cube):

        def get_char(i: int) -> str:
            if 18 <= i <= 26: return 'x'
            return {
                cube.squares[46]: 'a',
                cube.squares[30]: 'b',
                cube.squares[ 7]: 'c',
                cube.squares[14]: 'd'
            }[cube.squares[i]]

        indices = [
                6,  7,  8,
            11, 18, 19, 20, 27,
            14, 21, 22, 23, 30,
            17, 24, 25, 26, 33,
                45, 46, 47
        ]

        for _ in range(4):
            diagram = ''.join(get_char(i) for i in indices)
            if diagram in pll_dict: break
            cube.make_move(U)

        for move in pll_dict[diagram]:
            cube.make_move(move)
        
        # Final step: turn down face
        while not cube.edge_solved(0):
            cube.make_move(U)


# All 22 possible scenarios for PLL
pll_dict = {''.join(key): val for key, val in {

    # Aa
    (       'b','c','a',
        'c','x','x','x','d',
        'd','x','x','x','b',
        'c','x','x','x','b',
            'd','a','a',
    ): [L2, B2, Li, Fi, L, B2, Li, F, Li],

    # Ab
    (       'd','c','c',    
        'a','x','x','x','b',
        'd','x','x','x','b',
        'a','x','x','x','d',
            'b','a','c',
    ): [L2, F2, L, B, Li, F2, L, Bi, L],

    # F
    (       'a','c','b',    
        'd','x','x','x','c',
        'd','x','x','x','b',
        'd','x','x','x','a',
            'c','a','b',
    ): [Ri, Ui, Fi, R, U, Ri, Ui, Ri, F, R2, Ui, Ri, Ui, R, U, Ri, U, R],

    # Ga
    (       'd','c','a',    
        'b','x','x','x','c',
        'd','x','x','x','b',
        'b','x','x','x','d',
            'c','a','a',
    ): [R2, u, Ri, U, Ri, Ui, R, ui, R2, Fi, U, F],

    # Gb
    (       'a','c','d',    
        'c','x','x','x','b',
        'd','x','x','x','b',
        'c','x','x','x','a',
            'b','a','d',
    ): [Ri, Ui, R, B2, u, Bi, U, B, Ui, B, ui, B2],

    # Gc
    (       'a','c','c',    
        'b','x','x','x','d',
        'd','x','x','x','b',
        'b','x','x','x','a',
            'd','a','c',
    ): [R2, ui, R, Ui, R, U, Ri, u, R2, B, Ui, Bi],

    # Gd
    (       'b','c','d',    
        'a','x','x','x','c',
        'd','x','x','x','b',
        'a','x','x','x','b',
            'c','a','d',
    ): [R, U, Ri, F2, ui, F, Ui, Fi, U, Fi, u, F2],

    # Ja
    (       'a','c','c',    
        'd','x','x','x','b',
        'd','x','x','x','b',
        'c','x','x','x','b',
            'a','a','d',
    ): [Bi, U, Fi, U2, B, Ui, Bi, U2, B, F],

    # Jb
    (       'c','c','a',    
        'd','x','x','x','b',
        'd','x','x','x','b',
        'd','x','x','x','c',
            'b','a','a',
    ): [R, U, Ri, Fi, R, U, Ri, Ui, Ri, F, R2, Ui, Ri],

    # Ra
    (       'b','c','a',    
        'c','x','x','x','c',
        'd','x','x','x','b',
        'a','x','x','x','b',
            'd','a','d',
    ): [L, U2, Li, U2, L, Fi, Li, Ui, L, U, L, F, L2],

    # Rb
    (       'c','c','b',    
        'a','x','x','x','d',
        'd','x','x','x','b',
        'a','x','x','x','c',
            'd','a','b',
    ): [R2, F, R, U, R, Ui, Ri, Fi, R, U2, Ri, U2, R],

    # T
    (       'c','c','d',    
        'b','x','x','x','a',
        'd','x','x','x','b',
        'b','x','x','x','c',
            'a','a','d',
    ): [R, U, Ri, Ui, Ri, F, R2, Ui, Ri, Ui, R, U, Ri, Fi],

    # E
    (       'd','c','b',    
        'a','x','x','x','a',
        'd','x','x','x','b',
        'c','x','x','x','c',
            'd','a','b',
    ): [Li, B, L, Fi, Li, Bi, L, F, Li, Bi, L, Fi, Li, B, L, F],

    # Na
    (       'c','c','a',    
        'b','x','x','x','b',
        'd','x','x','x','b',
        'd','x','x','x','d',
            'c','a','a',
    ): [L, Ui, R, U2, Li, U, Ri, L, Ui, R, U2, Li, U, Ri],

    # Nb
    (       'a','c','c',    
        'd','x','x','x','d',
        'd','x','x','x','b',
        'b','x','x','x','b',
            'a','a','c',
    ): [Ri, U, Li, U2, R, Ui, L, Ri, U, Li, U2, R, Ui, L],

    # V
    (       'a','c','b',    
        'c','x','x','x','c',
        'd','x','x','x','b',
        'd','x','x','x','d',
            'a','a','b',
    ): [Ri, U, Ri, Ui, Bi, Ri, B2, Ui, Bi, U, Bi, R, B, R],

    # Y
    (       'a','c','d',    
        'b','x','x','x','b',
        'd','x','x','x','b',
        'c','x','x','x','c',
            'a','a','d',
    ): [F, Ri, F, R2, Ui, Ri, Ui, R, U, Ri, Fi, R, U, Ri, Ui, Fi],

    # H
    (       'a','c','a',    
        'b','x','x','x','d',
        'd','x','x','x','b',
        'b','x','x','x','d',
            'c','a','c',
    ): [M2, U, M2, U2, M2, U, M2],

    # Ua
    (       'c','c','c',    
        'b','x','x','x','a',
        'd','x','x','x','b',
        'b','x','x','x','a',
            'd','a','d',
    ): [M2, U, M, U2, Mi, U, M2],

    # Ub
    (       'c','c','c',    
        'a','x','x','x','d',
        'd','x','x','x','b',
        'a','x','x','x','d',
            'b','a','b',
    ): [M2, Ui, M, U2, Mi, Ui, M2],

    # Z
    (       'b','c','b',    
        'a','x','x','x','c',
        'd','x','x','x','b',
        'a','x','x','x','c',
            'd','a','d',
    ): [Mi, U, M2, U, M2, U, Mi, U2, M2],

    # Already solved
    (       'c','c','c',    
        'd','x','x','x','b',
        'd','x','x','x','b',
        'd','x','x','x','b',
            'a','a','a',
    ): []
}.items()}
