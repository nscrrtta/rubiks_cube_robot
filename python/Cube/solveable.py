from collections import Counter
from Util.path_finder import PathFinder
from .constants import F, Fi, B, Bi
from .cube import Cube


class Solveable:

    def __init__(self, cube: Cube):
        self.cube = cube


    def is_solveable(self) -> bool:
        return (
            self._count_colours()
            and self._corners_valid()
            and self._edges_valid()
            and self._even_swaps()
        )
    

    def _count_colours(self) -> bool:
        counts = Counter(self.cube.squares)
        return all(counts[i] == 9 for i in range(6))
            

    def _corners_valid(self) -> bool:
        self.c_dict = {}
        for i in range(8):
            j = self.cube.find_corner(i)
            if j is None: return False

            a = self.cube._solved_corners()[i]
            b = self.cube._current_corners()[j]
            if not self._can_rotate_to(a, b):
                return False
            
            self.c_dict[i] = j
        return self._sum_corners() % 3 == 0
    

    def _can_rotate_to(self, a: tuple[int], b: tuple[int]) -> bool:
        for _ in range(3):
            if a == b: return True
            a = (a[1], a[2], a[0])
        return False


    def _sum_corners(self) -> int:
        sum_corners = 0
        colours = [self.cube.squares[i] for i in (22, 40)] # U, D
        for _ in range(4):
            if self.cube.squares[33] in colours: sum_corners += 1
            if self.cube.squares[47] in colours: sum_corners += 2
            if self.cube.squares[53] in colours: sum_corners += 1
            if self.cube.squares[35] in colours: sum_corners += 2
            self.cube.rotate_y_axis()
        return sum_corners
    

    def _edges_valid(self) -> bool:
        self.e_dict = {}
        flips = 0
        for i in range(12):
            j = self.cube.find_edge(i)
            if j is None: return False
            flips += self._path_exists(j, i)
            self.e_dict[i] = j
        return flips % 2 == 0
    

    def _path_exists(self, start: int, final: int) -> int:
        return len(PathFinder.find_paths(
            cube=self.cube,
            find_one=True,
            start_node=start,
            final_node=final,
            move_limit=2,
            prohibited={F, Fi, B, Bi}
        ))


    def _even_swaps(self) -> bool:
        swaps = self._count_swaps(self.e_dict)
        swaps += self._count_swaps(self.c_dict)
        return swaps % 2 == 0


    def _count_swaps(self, d: dict) -> int:
        for i, j in d.items():
            if i == j: continue
            d[i], d[j] = d[j], d[i]
            return 1 + self._count_swaps(d)
        return 0
