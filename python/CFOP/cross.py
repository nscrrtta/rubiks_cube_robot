from Util.path_finder import PathFinder
from Cube.constants import *
from Cube.cube import Cube
import itertools


class Cross:
    
    def __init__(self, max_solves=MAX_SOLVE_CROSS):
        self.max_solves = max_solves
    

    def solve_cross(self, cube: Cube) -> list[Cube]:
        self.solved_cubes: list[Cube] = []
        self.solved_count = 0

        edges = [cube.squares[i] for i in (4, 13, 31, 49)] # B, L, R, F
        for permutation in itertools.permutations(edges):
            self._solve_cross_recursively(cube.spawn_child(), permutation)

        return self.solved_cubes

    
    def _solve_cross_recursively(self, cube: Cube, edges: list[int], depth=0):
        if self.solved_count >= self.max_solves:
            return
        if depth == len(edges):
            self.solved_cubes.append(cube)
            self.solved_count += 1
            return
        
        for cube in self._get_cubes_with_solved_edge(cube, edges[depth]):
            self._solve_cross_recursively(cube, edges, depth + 1)
    

    def _get_cubes_with_solved_edge(self, cube: Cube, edge: int) -> list[Cube]:
        cubes: list[Cube] = []

        # Rotate cube so correct face is in front
        while cube.squares[49] != edge:
            cube.rotate_y_axis()

        # If edge already solved
        if cube.edge_solved(0):
            return [cube]

        # Locate current edge node
        start = cube.find_edge(0)

        options = self._get_paths_that_keep_cross(cube, start) \
               or self._get_paths_that_undo_cross(cube, start)
        
        for moves in options:
            child = cube.spawn_child()
            for move in moves: child.make_move(move)
            cubes.append(child)

        return cubes


    def _get_paths_that_keep_cross(self, cube: Cube, start: int) -> list[tuple[str]]:
        prohibited = set()

        if cube.edge_solved(1):
            prohibited |= {R, R2, Ri}
        if cube.edge_solved(2):
            prohibited |= {B, B2, Bi}
        if cube.edge_solved(3):
            prohibited |= {L, L2, Li}
        if prohibited:
            prohibited |= {U, U2, Ui}

        return self._find_paths(cube, start, 3, prohibited) \
            or self._find_paths(cube, start, 4, prohibited)


    def _get_paths_that_undo_cross(self, cube: Cube, start: int)  -> list[tuple[str]]:
        # These paths undo the cross to solve an edge then fix the cross
        if start == 0:
            return [(Fi, L, D, Li, F2), (F, Ri, Di, R, F2), (Fi, U, Li, Ui), (F, Ui, R, U)]
        elif start == 2:
            return [(B2, Di, R, Fi, Ri), (B2, D, Li, F, L)]
        elif start == 4:
            return [(L, D, Li, F2), (U, Li, Ui)]
        elif start == 5:
            return [(Ri, Di, R, F2), (Ui, R, U)]
        elif start == 6 and cube.squares[5] == cube.squares[22]:
            return [(R, Di, Ri, F2), (R, Di, F2, Ri), (Ui, Ri, U)]
        elif start == 6 and cube.squares[28] == cube.squares[22]:
            return [(R2, Fi, R2), (Bi, D2, F2, B)]
        elif start == 7 and cube.squares[3] == cube.squares[22]:
            return [(Li, D, L, F2), (Li, D, F2, L), (U, L, Ui)]
        elif start == 7 and cube.squares[10] == cube.squares[22]:
            return [(L2, F, L2), (B, D2, F2, Bi)]
        elif start == 8:
            return [(D, R, Fi, Ri), (Di, Li, F, L)]
        elif start == 9:
            return [(R, Fi, Ri)]
        elif start == 10:
            return [(Di, R, Fi, Ri), (D, Li, F, L)]
        elif start == 11:
            return [(Li, F, L)]


    def _find_paths(self, cube: Cube, start: int, limit: int, prohibited: set) -> list[tuple[str]]:
        return PathFinder.find_paths(
            cube=cube,
            find_one=False,
            start_node=start,
            final_node=0,
            move_limit=limit,
            prohibited=prohibited,
        )
