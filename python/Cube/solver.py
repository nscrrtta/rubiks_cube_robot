from Util.move_manager import MoveManager
from CFOP.cross import Cross
from CFOP.f2l import F2L
from CFOP.oll import OLL
from CFOP.pll import PLL
from .constants import *
from .cube import Cube
import random
import time


class Solver:

    def __init__(self, cube: Cube):
        self.cube = cube

        self.cross = Cross()
        self.f2l = F2L()
        self.oll = OLL()
        self.pll = PLL()


    def solve(self) -> list[tuple[str]]:
        t = time.time()

        cubes = self.cross.solve_cross(self.cube)
        cubes = self._get_best_cubes(cubes, *NUM_CUBES_CROSS)

        # Rotate cubes up-side-down
        for cube in cubes: cube.rotate_z_axis(2)

        cubes = self.f2l.solve_f2l(cubes)
        cubes = self._get_best_cubes(cubes, NUM_CUBES_F2L)

        self.oll.solve_oll(cubes)
        self.pll.solve_pll(cubes)

        moves = self._get_best_cubes(cubes, 1)[0].moves
        
        print(f'{len(moves)} moves in {round(time.time()-t, 2)} seconds')
        for i in range(0, len(moves), 10): print(moves[i : i + 10])
        print()

        return MoveManager.convert_to_pairs(moves)
    

    def _get_best_cubes(self, cubes: list[Cube], n: int, m=0) -> list[Cube]:
        """
        Return a list of n cubes:
            - moves reduced, U moves replaced
            - sorted by number of moves
            - deduped 
        
        Include m cubes that have U moves
        """
        if m == 0: return self._sort_and_dedupe(cubes, n)
        
        # Split cubes into two lists
        cubes_u: list[Cube] = [] # Cubes with U moves
        cubes_x: list[Cube] = [] # Cubes without U moves

        for cube in cubes:
            u = any(moves[0] == 'U' for moves in cube.moves)
            cubes_u.append(cube) if u else cubes_x.append(cube)
        
        # Get m cubes with U moves, n cubes without U moves
        cubes_u = self._sort_and_dedupe(cubes_u, m)
        cubes_x = self._sort_and_dedupe(cubes_x, n)

        # Cubes with U moves: only include cubes with less than 20 moves
        i = 0
        while i < len(cubes_u) and len(cubes_u[i].moves) < 20:
            i += 1
        
        return cubes_u[:i] + cubes_x[:n-i]
   

    def _sort_and_dedupe(self, cubes: list[Cube], n: int) -> list[Cube]:
        for cube in cubes:
            cube.moves = MoveManager.replace_u_moves(cube.moves)
            cube.moves = MoveManager.reduce_moves(cube.moves)

        # Sort by number of moves
        cubes = sorted(cubes, key=lambda cube: len(cube.moves))

        # Remove duplicates (cubes with the same moves)
        seen = set()
        deduped_cubes = []
        for cube in cubes:
            moves = tuple(cube.moves)
            if moves not in seen:
                seen.add(moves)
                deduped_cubes.append(cube)
            if len(deduped_cubes) == n: break

        return deduped_cubes
    

    def scramble(self) -> list[tuple[str]]:
        moves = []

        while len(moves) < 20:
            face = random.choice(['F', 'B', 'L', 'R', 'D'])
            turn = random.choice(['1', '2', '3'])

            moves.append(face + turn)
            moves = MoveManager.reduce_moves(moves)

        print(f'scramble: {moves}')
        return MoveManager.convert_to_pairs(moves)
