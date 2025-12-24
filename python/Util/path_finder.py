from Util.move_manager import MoveManager
from Cube.constants import *
from Cube.cube import Cube


# Moves that link two edges
links = {
    0: { 3: U,  2: U2,  1: Ui,  5: F,  8: F2,  4: Fi},
    1: { 0: U,  3: U2,  2: Ui,  6: R,  9: R2,  5: Ri},
    2: { 1: U,  0: U2,  3: Ui,  7: B, 10: B2,  6: Bi},
    3: { 2: U,  1: U2,  0: Ui,  4: L, 11: L2,  7: Li},
    4: { 0: F,  5: F2,  8: Fi, 11: L,  7: L2,  3: Li},
    5: { 8: F,  4: F2,  0: Fi,  1: R,  6: R2,  9: Ri},
    6: { 2: B,  7: B2, 10: Bi,  9: R,  5: R2,  1: Ri},
    7: {10: B,  6: B2,  2: Bi,  3: L,  4: L2, 11: Li},
    8: { 9: D, 10: D2, 11: Di,  4: F,  0: F2,  5: Fi},
    9: {10: D, 11: D2,  8: Di,  5: R,  1: R2,  6: Ri},
    10:{11: D,  8: D2,  9: Di,  6: B,  2: B2,  7: Bi},
    11:{ 8: D,  9: D2, 10: Di,  7: L,  3: L2,  4: Li},
}


class PathFinder:

    def find_paths(
            cube: Cube,
            find_one: bool,
            start_node: str,
            final_node: str,
            move_limit: int,
            prohibited: set,
        ) -> list[tuple[str]]:
        
        current_moves: list[str] = []
        visited_nodes = set()
        options = set()
 
        def search(curr_node):
            if len(current_moves) > move_limit:
                return
            if find_one and options:
                return
            if curr_node == final_node:
                moves = tuple(MoveManager.reduce_moves(current_moves))
                if moves in options: return

                # Check if these moves solve edge
                child = cube.spawn_child()
                for move in moves: child.make_move(move, save=False)
                if child.edge_solved(final_node): options.add(moves)
                return
            
            for node, move in links[curr_node].items():
                if node in visited_nodes:
                    continue
                if move in prohibited:
                    continue
                current_moves.append(move)
                visited_nodes.add(node)
                search(node)
                current_moves.pop()
                visited_nodes.remove(node)
                    
        search(start_node)
        return sorted(options, key=lambda moves: len(moves))
