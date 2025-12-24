from Cube.constants import *
from Cube.cube import Cube
import itertools


class F2L:

    def __init__(self, max_solves=MAX_SOLVE_F2L):
        self.max_solves = max_solves


    def solve_f2l(self, cubes: list[Cube]) -> list[Cube]:
        self.solved_cubes: list[Cube] = []

        for cube in cubes:
            self.solved_count = 0
            edges = [cube.squares[i] for i in (4, 13, 31, 49)] # B, L, R, F
            for permutation in itertools.permutations(edges):
                self._solve_f2l_recursively(cube.spawn_child(), permutation)

        return self.solved_cubes
    

    def _solve_f2l_recursively(self, cube: Cube, edges: list[int], depth=0):
        if self.solved_count >= self.max_solves:
            return
        if depth == len(edges):
            self.solved_cubes.append(cube)
            self.solved_count += 1
            return
        
        for cube in self._get_cubes_with_solved_pair(cube, edges[depth]):
            self._solve_f2l_recursively(cube, edges, depth + 1)
        
    
    def _get_cubes_with_solved_pair(self, cube: Cube, edge: int) -> list[Cube]:
        cubes: list[Cube] = []

        # Rotate cube so correct face is in front
        while cube.squares[49] != edge:
            cube.rotate_y_axis()

        # If pair already solved
        if cube.edge_solved(5) and cube.corner_solved(5):
            return [cube]

        # Locate current corner node and edge node
        edge_node = cube.find_edge(5)
        crnr_node = cube.find_corner(5)

        # Rotate cube so corner is FRU or FRD (corner is 1 or 5)
        i = (crnr_node - 1) % 4
        j = (edge_node - i) % 4

        if i > 0: cube.rotate_y_axis(i)

        # Update corner node and edge node after rotating cube
        crnr_node = (crnr_node // 4) * 4 + 1
        edge_node = (edge_node // 4) * 4 + j
        
        if   crnr_node == 1: options = self._get_paths_corner_node_1(cube, edge_node)
        elif crnr_node == 5: options = self._get_paths_corner_node_5(cube, edge_node)

        for moves in options:
            child = cube.spawn_child()
            for move in moves: child.make_move(move)
            cubes.extend(self._get_cubes_with_solved_pair(child, edge))

        return cubes


    def _get_paths_corner_node_1(self, cube: Cube, edge_node: int) -> list[list[str]]:
        options: list[list[str]] = []

        if edge_node == 0:
            # White faces up
            if cube.squares[26] == cube.squares[40]:

                # Front-facing colours are the same
                if cube.squares[46] == cube.squares[47]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.extend([[U2, Li, U, L, Ui, F, Ui, Fi], [U2, Li, Ui, L, Ui, F, Ui, Fi]])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.extend([[U, Fi, U, F, Ui, R, Ui, Ri], [U, Fi, Ui, F, Ui, R, Ui, Ri]])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.extend([[Ri, U, R, Ui, B, Ui, Bi], [Ri, Ui, R, Ui, B, Ui, Bi]])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.extend([[Ui, Bi, U, B, Ui, L, Ui, Li], [Ui, Bi, Ui, B, Ui, L, Ui, Li]])

                # Front-facing colours are different
                else:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U, Li, U2, L])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([Fi, U2, F])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ui, Ri, U2, R])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U2, Bi, U2, B])
                    
            # White faces right
            elif cube.squares[33] == cube.squares[40]:

                # Front-facing colours are different
                if cube.squares[46] != cube.squares[47]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U2, Li, U2, L])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([U, Fi, U2, F])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ri, U2, R])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([Ui, Bi, U2, B])
                   
                # Front-facing colours are the same
                elif cube.squares[46] == cube.squares[49]:
                    options = [[Ui, Fi, U, F]]
                elif cube.squares[46] == cube.squares[31]:
                    options = [[U, Ri, U2, R]]
                elif cube.squares[46] == cube.squares[13]:
                    options = [[Li, U, L]]
                elif cube.squares[46] == cube.squares[ 4]:
                    options = [[U, Bi, U, B], [Bi, U2, B]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:

                first_move = [Ui] if cube.squares[23] == cube.squares[26] else []

                if not (cube.corner_solved(4) and cube.edge_solved(4)):
                    options.append(first_move + [U2, Li, U, L])
                if not (cube.corner_solved(5) and cube.edge_solved(5)):
                    options.append(first_move + [U, Fi, U, F])
                if not (cube.corner_solved(6) and cube.edge_solved(6)):
                    options.append(first_move + [Ri, U, R])
                if not (cube.corner_solved(7) and cube.edge_solved(7)):
                    options.append(first_move + [Ui, Bi, U, B])
    
        elif edge_node == 1:
            # White faces up
            if cube.squares[26] == cube.squares[40]:

                # Right-facing colours are the same
                if cube.squares[30] == cube.squares[33]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.extend([[F, Ui, Fi, U, Li, U, L], [F, U, Fi, U, Li, U, L]])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.extend([[Ui, R, Ui, Ri, U, Fi, U, F], [Ui, R, U, Ri, U, Fi, U, F]])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.extend([[U2, B, Ui, Bi, U, Ri, U, R], [U2, B, U, Bi, U, Ri, U, R]])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.extend([[U, L, Ui, Li, U, Bi, U, B], [U, L, U, Li, U, Bi, U, B]])

                # Right-facing colours are different
                else:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U, F, U2, Fi])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([R, U2, Ri])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ui, B, U2, Bi])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U2, L, U2, Li])
                            
            # White faces right
            elif cube.squares[33] == cube.squares[40]:

                first_move = [U] if cube.squares[23] == cube.squares[26] else []

                if not (cube.corner_solved(4) and cube.edge_solved(4)):
                    options.append(first_move + [F, Ui, Fi])
                if not (cube.corner_solved(5) and cube.edge_solved(5)):
                    options.append(first_move + [Ui, R, Ui, Ri])
                if not (cube.corner_solved(6) and cube.edge_solved(6)):
                    options.append(first_move + [U2, B, Ui, Bi])
                if not (cube.corner_solved(7) and cube.edge_solved(7)):
                    options.append(first_move + [U, L, Ui, Li])

            # White faces front
            elif cube.squares[47] == cube.squares[40]:

                # Right-facing colours are different
                if cube.squares[30] != cube.squares[33]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([F, U2, Fi])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([Ui, R, U2, Ri])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([U2, B, U2, Bi])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U, L, U2, Li])
            
                # Right-facing colours are the same -> solve pair
                elif cube.squares[30] == cube.squares[49]:
                    options = [[U2, F, Ui, Fi]]
                elif cube.squares[30] == cube.squares[31]:
                    options = [[U, R, Ui, Ri]]
                elif cube.squares[30] == cube.squares[13]:
                    options = [[Ui, L, Ui, Li], [L, U2, Li]]
                elif cube.squares[30] == cube.squares[ 4]:
                    options = [[B, Ui, Bi]]
        
        elif edge_node == 2:
            # White faces up
            if cube.squares[26] == cube.squares[40]:

                # Front-facing and up-facing colours are the same
                if cube.squares[19] == cube.squares[47]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U, Li, U, L])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([Fi, U, F])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ui, Ri, U, R])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U2, Bi, U, B])

                # Front-facing and up-facing colours are different -> solve pair
                elif cube.squares[7] == cube.squares[49]:
                    options = [[U2, F, U2, Fi, U, F, Ui, Fi]]
                elif cube.squares[7] == cube.squares[31]:
                    options = [[U, R, U2, Ri, U, R, Ui, Ri]]
                elif cube.squares[7] == cube.squares[13]:
                    options = [[Ui, L, U2, Li, U, L, Ui, Li]]
                elif cube.squares[7] == cube.squares[ 4]:
                    options = [[B, U2, Bi, U, B, Ui, Bi]]

            # White faces right
            elif cube.squares[33] == cube.squares[40]:

                # Top-facing colours are the same
                if cube.squares[19] == cube.squares[26]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U2, Li, U2, L])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([U, Fi, U2, F])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ri, U2, R])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([Ui, Bi, U2, B])

                # Top-facing colours are different -> solve pair
                elif cube.squares[47] == cube.squares[49]:
                    options = [[R, U, Ri]]
                elif cube.squares[47] == cube.squares[31]:
                    options = [[Ui, B, U, Bi]]
                elif cube.squares[47] == cube.squares[13]:
                    options = [[U, F, U, Fi]]
                elif cube.squares[47] == cube.squares[ 4]:
                    options = [[U2, L, U, Li]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:

                u_move = U if cube.squares[19] == cube.squares[26] else Ui

                if not (cube.corner_solved(4) and cube.edge_solved(4)):
                    options.append([F, u_move, Fi])
                if not (cube.corner_solved(5) and cube.edge_solved(5)):
                    options.append([Ui, R, u_move, Ri])
                if not (cube.corner_solved(6) and cube.edge_solved(6)):
                    options.append([U2, B, u_move, Bi])
                if not (cube.corner_solved(7) and cube.edge_solved(7)):
                    options.append([Ui, L, u_move, Li])

        elif edge_node == 3:
            # White faces up
            if cube.squares[26] == cube.squares[40]:

                # Front-facing and up-facing colours are different
                if cube.squares[21] != cube.squares[47]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([U, F, Ui, Fi])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([R, Ui, Ri])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([Ui, B, Ui, Bi])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U2, L, Ui, Li])
                
                # Front-facing and up-facing colours are the same -> solve pair
                elif cube.squares[14] == cube.squares[49]:
                    options = [[Ui, Fi, U2, F, Ui, Fi, U, F]]
                elif cube.squares[14] == cube.squares[31]:
                    options = [[U2, Ri, U2, R, Ui, Ri, U, R]]
                elif cube.squares[14] == cube.squares[13]:
                    options = [[Li, U2, L, Ui, Li, U, L]]
                elif cube.squares[14] == cube.squares[ 4]:
                    options = [[U, Bi, U2, B, Ui, Bi, U, B]]
                
            # White faces right
            elif cube.squares[33] == cube.squares[40]:
                
                u_move = Ui if cube.squares[21] == cube.squares[26] else U

                if not (cube.corner_solved(4) and cube.edge_solved(4)):
                    options.append([U2, Li, u_move, L])
                if not (cube.corner_solved(5) and cube.edge_solved(5)):
                    options.append([U, Fi, u_move, F])
                if not (cube.corner_solved(6) and cube.edge_solved(6)):
                    options.append([Ri, u_move, R])
                if not (cube.corner_solved(7) and cube.edge_solved(7)):
                    options.append([U, Bi, u_move, B])
            
            # White faces front
            elif cube.squares[47] == cube.squares[40]:

                # Top-facing colours are the same
                if cube.squares[21] == cube.squares[26]:
                    if not (cube.corner_solved(4) and cube.edge_solved(4)):
                        options.append([F, U2, Fi])
                    if not (cube.corner_solved(5) and cube.edge_solved(5)):
                        options.append([Ui, R, U2, Ri])
                    if not (cube.corner_solved(6) and cube.edge_solved(6)):
                        options.append([U2, B, U2, Bi])
                    if not (cube.corner_solved(7) and cube.edge_solved(7)):
                        options.append([U, L, U2, Li])
                    
                # Top-facing colours are different -> solve pair
                elif cube.squares[26] == cube.squares[49]:
                    options = [[Fi, Ui, F]]
                elif cube.squares[26] == cube.squares[31]:
                    options = [[Ui, Ri, Ui, R]]
                elif cube.squares[26] == cube.squares[13]:
                    options = [[U, Li, Ui, L]]
                elif cube.squares[26] == cube.squares[ 4]:
                    options = [[U2, Bi, Ui, B]]

        elif edge_node == 4:
            # White faces up
            if cube.squares[26] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[47] == cube.squares[48]:
                    options = [[L, Fi, Li, F]]
                # Front-facing colours are different
                else: options = [[U, F, Ui, Fi], [U, Li, U, L]]

            # White faces right
            elif cube.squares[33] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[47] == cube.squares[48]:
                    options = [[Ui, Li, U, L]]
                # Front-facing colours are different
                else: options = [[F, U2, Fi]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:
                # Top-facing and front-facing colours are the same
                if cube.squares[26] == cube.squares[48]:
                    options = [[F, U, Fi]]
                # Top-facing and front-facing colours are different
                else: options = [[Li, Ui, L]]

        elif edge_node == 5:
            # White faces up
            if cube.squares[26] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[47] == cube.squares[50]:
                    options = [[R, Ui, Ri], [Fi, U, F]]
                # Front-facing colours are different
                else: options = [[U, Ri, F, R, Fi], [Ui, F, Ri, Fi, R]]

            # White faces right
            elif cube.squares[33] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[47] == cube.squares[50]:
                    options = [[U, R, U, Ri], [U, Fi, U, F]]
                # Front-facing colours are different
                else: options = [[U, Fi, Ui, F]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[33] == cube.squares[34]:
                    options = [[Ui, Fi, Ui, F]]
                # Right-facing colours are different
                else: options = [[Ui, R, U, Ri]]

        elif edge_node == 6:
            # White faces up
            if cube.squares[26] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[33] == cube.squares[28]:
                    options = [[Bi, R, B, Ri]]
                # Right-facing colours are different
                else: options = [[Ui, Ri, U, R]]

            # White faces right
            elif cube.squares[33] == cube.squares[40]:
                # Front-facing and right-facing colours are the same
                if cube.squares[47] == cube.squares[28]:
                    options = [[B, U, Bi]]
                # Front-facing and right-facing colours are different
                else: options = [[Ri, Ui, R]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[33] == cube.squares[28]:
                    options = [[U, B, Ui, Bi]]
                # Right-facing colours are different
                else: options = [[Ri, U2, R]]

        elif edge_node == 7:
            # White faces up
            if cube.squares[26] == cube.squares[40]:
                # Front-facing and back-facing colours are the same
                if cube.squares[47] == cube.squares[3]:
                    options = [[U2, L, Ui, Li], [U2, Bi, U, B]]
                # Front-facing and back-facing colours are different
                else: options = [[U, B, Li, Bi, L], [Ui, Li, B, L, Bi]]

            # White faces right
            elif cube.squares[33] == cube.squares[40]:
                # Front-facing and back-facing colours are the same
                if cube.squares[47] == cube.squares[3]:
                    options = [[Ui, L, U, Li]]
                # Front-facing and back-facing colours are different
                else: options = [[Bi, U, B]]

            # White faces front
            elif cube.squares[47] == cube.squares[40]:
                # Right-facing and left-facing colours are the same
                if cube.squares[33] == cube.squares[10]:
                    options = [[U, Bi, Ui, B]]
                # Right-facing and left-facing colours are different
                else: options = [[L, Ui, Li]]

        return options


    def _get_paths_corner_node_5(self, cube: Cube, edge_node: int) -> list[list[str]]:
        options: list[list[str]] = []

        if edge_node == 0:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[53] == cube.squares[46]:
                    options = [[U, R, Ui, Ri], [U, R, U, Ri]]
                # Front-facing colours are different
                else: options = [[Fi, U2, F]]
            
            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[53] == cube.squares[46]:
                    options = [[U, Fi, U, F], [Ui, R, U, Ri]]
                # Front-facing colours are different -> solve pair
                elif cube.squares[46] == cube.squares[13]:
                    options = [[R, Li, U, L, Ri]]
                # Right-facing colours are different -> don't solve pair
                else: options = [[R, U, Ri]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing and front-facing colours are the same
                if cube.squares[35] == cube.squares[46]:
                    options = [[Fi, Ui, F]]
                # Right-facing and front-facing colours are different
                else: options = [[Ui]]
        
        elif edge_node == 1:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[35] == cube.squares[30]:
                    options = [[Ui, Fi, U, F], [Ui, Fi, Ui, F]]
                # Right-facing colours are different
                else: options = [[R, U2, Ri]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing and top-facing colours are the same
                if cube.squares[53] == cube.squares[23]:
                    options = [[U]]
                # Front-facing and top-facing colours are different
                else: options = [[R, U, Ri]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[35] == cube.squares[30]:
                    options = [[Ui, R, Ui, Ri], [U, Fi, Ui, F]]
                # Right-facing colours are different -> solve pair
                elif cube.squares[30] == cube.squares[4]:
                    options = [[Fi, B, Ui, Bi, F]]
                # Right-facing colours are different -> don't solve pair
                else: options = [[Fi, Ui, F]]

        elif edge_node == 2:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing and top-facing colours are the same
                if cube.squares[19] == cube.squares[53]:
                    options = [[Fi, U, F], [Fi, Ui, F]]
                # Front-facing and top-facing colours are different
                else: options = [[Ui, R, U, Ri]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing and top-facing colours are the same
                if cube.squares[19] == cube.squares[53]:
                    options = [[U2]]
                # Front-facing and top-facing colours are different
                else: options = [[R, U2, Ri], [U, R, U, Ri]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing and top-facing colours are the same
                if cube.squares[19] == cube.squares[35]:
                    options = [[U]]
                # Right-facing and top-facing colours are different
                else: options = [[R, Ui, Ri]]

        elif edge_node == 3:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing and left-facing colours are the same
                if cube.squares[53] == cube.squares[14]:
                    options = [[R, Ui, Ri], [R, U, Ri]]
                # Front-facing and left-facing colours are different
                else: options = [[U, Fi, Ui, F]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing and left-facing colours are the same
                if cube.squares[53] == cube.squares[14]:
                    options = [[Fi, U, F]]
                # Front-facing and left-facing colours are different
                else: options = [[Ui]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing and left-facing colours are the same
                if cube.squares[35] == cube.squares[14]:
                    options = [[Fi, U2, F], [Ui, Fi, Ui, F]]
                # Right-facing and left-facing colours are different
                else: options = [[U2]]

        elif edge_node == 4:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[48] == cube.squares[53]:
                    options = [[Fi, U, F2, U, Fi], [F, U, Fi, R, U, Ri], [Li, U, L, Fi, Ui, F]]
                # Front-facing colours are different
                else: options = [[Li, R, Ui, Ri, L]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[48] == cube.squares[53]:
                    options = [[Li, Ui, L]]
                # Front-facing colours are different
                else: options = [[F, U, Fi, Ui]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing and left-facing colours are the same
                if cube.squares[35] == cube.squares[16]:
                    options = [[F, Ui, Fi]]
                # Right-facing and left-facing colours are different
                else: options = [[Li, U2, L]]

        elif edge_node == 5:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing colours are different
                if cube.squares[50] != cube.squares[53]:
                    options = [[R, Ui, Ri], [Fi, U, F]]
                # Front-facing colours are the same and pair not already solved
                elif cube.squares[50] != cube.squares[49]:
                    options = [[R, U, Ri], [Fi, Ui, F]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing colours are the same
                if cube.squares[50] == cube.squares[53]:
                    options = [[R, Ui, Ri, Fi, U, F]]
                # Front-facing colours are different
                else: options = [[R, Ui, Ri]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[34] == cube.squares[35]:
                    options = [[Fi, U, F, R, Ui, Ri]]
                # Right-facing colours are different
                else: options = [[Fi, U, F]]

        elif edge_node == 6:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[28] == cube.squares[35]:
                    options = [[B, Ui, Bi, R, U, Ri]]
                # Right-facing colours are different
                else: options = [[Fi, B, U, Bi, F]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing and right-facing colours are the same
                if cube.squares[53] == cube.squares[28]:
                    options = [[R, U, R2, U, R], [Fi, Ui, F]]
                # Front-facing and right-facing colours are different
                else: options = [[Ri, U, R2, U, Ri], [B, U, Bi, R, U, Ri]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Right-facing colours are the same
                if cube.squares[28] == cube.squares[35]:
                    options = [[B, U, Bi]]
                # Right-facing colours are different
                else: options = [[Ri, U, R, Ui], [B, Ui, Bi, Fi, U2, F]]

        elif edge_node == 7:
            # White faces down
            if cube.squares[42] == cube.squares[40]:
                # Front-facing and left-facing colours are the same
                if cube.squares[53] == cube.squares[10]:
                    options = [[L, R, U, Ri, Li]]
                # Front-facing and left-facing colours are different
                else: options = [[L, U, Li, Fi, Ui, F], [Bi, Ui, B, R, U, Ri]]

            # White faces right
            elif cube.squares[35] == cube.squares[40]:
                # Front-facing and left-facing colours are the same
                if cube.squares[53] == cube.squares[10]:
                    options = [[R, U, Ri, L, U2, Li], [Bi, U2, B, Fi, U, F]]
                # Front-facing and left-facing colours are different
                else: options = [[L, Ui, Li]]

            # White faces front
            elif cube.squares[53] == cube.squares[40]:
                # Down-facing and left-facing colours are the same 
                if cube.squares[42] == cube.squares[10]:
                    options = [[L, U2, Li]]
                # Down-facing and left-facing colours are different
                else: options = [[Bi, U, B]]

        return options
