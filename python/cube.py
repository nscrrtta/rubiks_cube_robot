from solveable import Solveable
from constants import *
from cfop import CFOP
import itertools
import random


class Cube(Solveable, CFOP):

    def solve(self) -> list[str]:
        initial_cube = [Cube(self.sqrs[:], self.centers, self.moves[:])]

        solved_cubes = self.search('C', initial_cube)
        solved_cubes = self.search('F', solved_cubes)

        for cube in solved_cubes:
            cube.OLL(); cube.PLL()
            cube.organize_moves(cube.moves, no_U=True)

        return min(solved_cubes, key=lambda x: len(x.moves)).moves
    

    def scramble(self) -> list[str]:
        moves = []
        while len(moves) < 20:
            face = random.choice(['F','B','L','R','D'])
            turn = random.choice(['1','2','3'])
            moves.append(face+turn)
            self.organize_moves(moves)
        return moves
    

    def search(self, step:str, cubes:list[CFOP]) -> list[CFOP]:
        """
        step = 'C': -> solving cross | 'cubes' is a list of a one scrambled cube
        step = 'F': -> solving F2L   | 'cubes' is a list of cubes with solved crosses

        n: Number of cubes returned
        """

        solved_cubes:list[CFOP] = []

        for permutation in itertools.permutations([self.F_col, self.R_col, self.B_col, self.L_col]):
            for cube in cubes:
                c = Cube(cube.sqrs[:], cube.centers, cube.moves[:])
                if step == 'C': c.cross(permutation, solved_cubes)
                elif step == 'F': c.F2L(permutation, solved_cubes)

        # Remove U/U2/Ui moves
        for cube in solved_cubes: cube.organize_moves(cube.moves, no_U=True)

        # Remove duplicates
        i = 0
        while i < len(solved_cubes):
            cube_i = solved_cubes[i]
            j = i+1
            while j < len(solved_cubes):
                cube_j = solved_cubes[j]
                if cube_i.moves == cube_j.moves:
                    del solved_cubes[j]
                else: j += 1
            i += 1

        # Sort in order of number of moves and return first n cubes
        n = {'C': CROSS_EXPLORATION_LIMIT, 'F': F2L_EXPLORATION_LIMIT}[step]
        return sorted(solved_cubes, key=lambda x: len(x.moves))[:n]
     