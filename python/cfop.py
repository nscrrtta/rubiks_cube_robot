from parent import Parent
from constants import *


class CFOP(Parent):    

    def cross(self, permutation:list, solved_cubes:list):

        # If reached max number of solutions
        if self.cubes_solved >= CROSS_PERMUTATION_LIMIT:
            return

        # If all edges solved
        if len(permutation) == 0:
            solved_cubes.append(CFOP(self.sqrs,self.centers,self.moves))
            self.cubes_solved += 1
            return
        
        # Front-facing colour
        F_col = permutation[0]

        # Rotate cube so home position of edge is FU (index 0)
        while self.sqrs[49] != F_col: self.rotate_cube(self.sqrs, y)

        # Locate edge
        for start_node, edge in self.get_current_edges(self.sqrs).items():
            if {F_col, self.U_col}.issubset(set(edge)): break

        illegal_moves = []
        # If right edge is solved, don't move right face
        if (self.sqrs[31],self.sqrs[23]) == (self.sqrs[30],self.sqrs[22]): illegal_moves += [R,R2,Ri]
        # If back edge is solved, don't move back face
        if (self.sqrs[4], self.sqrs[19]) == (self.sqrs[7], self.sqrs[22]): illegal_moves += [B,B2,Bi]
        # If left edge is solved, don't move left face
        if (self.sqrs[13],self.sqrs[21]) == (self.sqrs[14],self.sqrs[22]): illegal_moves += [L,L2,Li]
        # If any edge is solved, don't move up face
        if illegal_moves: illegal_moves += [U,U2,Ui]

        for move_limit in range(2,5):
            # Get the smallest unique paths that solve this edge
            # without unsolving any other edges in the cross
            paths = self.get_paths('edge',start_node,0,move_limit,[],illegal_moves,(F_col, self.U_col))
            if paths: break
        else:
            # No paths of length <= 4 found
            # some paths are impossible with certain illegal moves
            # ex: if edge is in position 0 and flipped, it cannot be solved without moving L/R
            illegal_moves = [B2]
            if 9 <= start_node <= 11: illegal_moves += [B,Bi]
            paths = self.get_paths('edge',start_node,0,3,[],illegal_moves,(F_col, self.U_col))

            # Fix paths so cross is maintained
            for path in paths:
                # Paths that end in F,F2,Fi
                if path[-1] in [F,F2,Fi]:
                    if len(path) > 2 and 0<=start_node<=7: move, index = path[-3], -1
                    else: move, index = path[-2], len(path)
                # Paths that end in U,U2,Ui
                elif path[-1] in [U,U2,Ui]: move, index = path[-1], -2

                m,n = move[0], move[1]
                path.insert(index, f'{m}{4-int(n)}')

        # Explore all the paths
        for path in paths:

            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
            for move in path: self.make_move(move)
            self.cross(permutation[1:], solved_cubes) # Solve next edge
            self.sqrs, self.moves = sqrs_copy, moves_copy


    def F2L(self, permutation:list, solved_cubes:list):

        # If reached max number of solutions
        if self.cubes_solved >= F2L_PERMUTATION_LIMIT:
            return

        # If no more pairs left to solve
        if len(permutation) == 0:
            solved_cubes.append(CFOP(self.sqrs,self.centers,self.moves))
            self.cubes_solved += 1
            return
        
        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col: self.rotate_cube(self.sqrs, z)

        # Front-facing colour
        F_col = permutation[0]
        # Right-facing colour (when cube is up-side-down)
        if   F_col == self.F_col: R_col = self.L_col
        elif F_col == self.L_col: R_col = self.B_col
        elif F_col == self.B_col: R_col = self.R_col
        elif F_col == self.R_col: R_col = self.F_col

        # Locate corner
        for corner_node, corner in self.get_current_corners(self.sqrs).items():
            if {F_col, R_col, self.U_col}.issubset(set(corner)): break

        # Rotate cube so corner is FRU or FRD (corner_node is 1 or 5)
        if corner_node in [0,4]:
            self.rotate_cube(self.sqrs, yi)
            corner_node += 1
        elif corner_node in [2,6]:
            self.rotate_cube(self.sqrs, y)
            corner_node -= 1
        elif corner_node in [3,7]:
            self.rotate_cube(self.sqrs, y)
            self.rotate_cube(self.sqrs, y)
            corner_node -= 2

        # Locate edge
        for edge_node, edge in self.get_current_edges(self.sqrs).items():
            if {F_col, R_col}.issubset(set(edge)): break

        if corner_node == 1:

            if edge_node == 0:
                # White faces up
                if self.sqrs[26] == self.U_col:

                    # Front-facing colours are the same
                    if self.sqrs[46] == self.sqrs[47]: moves = [U, Fi, U, F]
                    # Front-facing colours are different
                    else: moves = [Fi, U2, F]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.FRD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy
                        
                # White faces right
                elif self.sqrs[33] == self.U_col:

                    # Front-facing colours are the same
                    if self.sqrs[46] == self.sqrs[47]:
                        while self.sqrs[46] != self.sqrs[13]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [Li, U, L]:
                            self.make_move(move)

                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.BRD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [Ri, U2, R]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

                # White faces front
                elif self.sqrs[47] == self.U_col:

                    # Top-facing colours are the same
                    if self.sqrs[25] == self.sqrs[26]: moves = [Ui, Ri, U, R]
                    # Top-facing colours are different
                    else: moves = [Ri, U, R]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.BRD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy
     
            elif edge_node == 1:
                # White faces up
                if self.sqrs[26] == self.U_col:

                    # Right-facing colours are the same
                    if self.sqrs[30] == self.sqrs[33]: moves = [Ui, R, Ui, Ri]
                    # Right-facing colours are different
                    else: moves = [R, U2, Ri]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.FRD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy
                                
                # White faces right
                elif self.sqrs[33] == self.U_col:

                    # Top-facing colours are the same
                    if self.sqrs[23] == self.sqrs[26]: moves = [R, Ui, Ri]
                    # Top-facing colours are different
                    else: moves = [Ui, R, Ui, Ri]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.FRD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy

                # White faces front
                elif self.sqrs[47] == self.U_col:

                    # Right-facing colours are the same
                    if self.sqrs[30] == self.sqrs[33]:
                        while self.sqrs[30] != self.sqrs[4]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [B, Ui, Bi]:
                            self.make_move(move)
                        
                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.FLD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [F, U2, Fi]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

            elif edge_node == 2:
                # White faces up
                if self.sqrs[26] == self.U_col:

                    # Front-facing and up-facing colours are the same
                    if self.sqrs[19] == self.sqrs[47]:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.FRD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [Fi, U, F]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

                    # Front-facing and up-facing colours are different
                    else:
                        while self.sqrs[7] != self.sqrs[4]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [B, U2, Bi, U, B, Ui, Bi]:
                            self.make_move(move)

                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

                # White faces right
                elif self.sqrs[33] == self.U_col:

                    # Top-facing colours are the same
                    if self.sqrs[19] == self.sqrs[26]:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.BRD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [Ri, U2, R]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

                    # Top-facing colours are different
                    else:
                        while self.sqrs[47] != self.sqrs[49]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [R, U, Ri]:
                            self.make_move(move)

                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

                # White faces front
                elif self.sqrs[47] == self.U_col:

                    # Top-facing colours are the same
                    if self.sqrs[19] == self.sqrs[26]: moves = [F, U, Fi]
                    # Top-facing colours are different
                    else: moves = [F, Ui, Fi]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.FLD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy

            elif edge_node == 3:
                # White faces up
                if self.sqrs[26] == self.U_col:

                    # Front-facing and up-facing colours are the same
                    if self.sqrs[21] == self.sqrs[47]:
                        while self.sqrs[14] != self.sqrs[13]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [Li, U2, L, Ui, Li, U, L]:
                            self.make_move(move)

                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

                    # Front-facing and up-facing colours are different
                    else:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.FRD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [R, Ui, Ri]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

                # White faces right
                elif self.sqrs[33] == self.U_col:
                    
                    # Top-facing colours are the same
                    if self.sqrs[21] == self.sqrs[26]: moves = [Ri, Ui, R]
                    # Top-facing colours are different
                    else: moves = [Ri, U, R]

                    for _ in range(4):
                        self.rotate_cube(self.sqrs, yi)
                        self.make_move(U)

                        if self.BRD_pair_solved(): continue

                        sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                        for move in moves: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                        self.sqrs, self.moves = sqrs_copy, moves_copy
                
                # White faces front
                elif self.sqrs[47] == self.U_col:

                    # Top-facing colours are the same
                    if self.sqrs[21] == self.sqrs[26]:
                        for _ in range(4):
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)

                            if self.FLD_pair_solved(): continue

                            sqrs_copy, moves_copy = self.sqrs[:], self.moves[:]
                            for move in [F, U2, Fi]: self.make_move(move)
                            self.F2L(permutation[:], solved_cubes)
                            self.sqrs, self.moves = sqrs_copy, moves_copy

                    # Top-facing colours are different
                    else:
                        while self.sqrs[26] != self.sqrs[49]:
                            self.rotate_cube(self.sqrs, yi)
                            self.make_move(U)
                        for move in [Fi, Ui, F]:
                            self.make_move(move)
                    
                        # Pair is solved -> solve next pair
                        self.F2L(permutation[1:], solved_cubes)

            elif edge_node == 4:
                # White faces up
                if self.sqrs[26] == self.U_col:

                    # Front-facing colours are the same
                    if self.sqrs[47] == self.sqrs[48]:
                        for move in [L, Fi, Li, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [U, F, Ui, Fi]: self.make_move(move)
                        # Other options: [U, Li, U, L]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[33] == self.U_col:

                    # Front-facing colours are the same
                    if self.sqrs[47] == self.sqrs[48]:
                        for move in [Ui, Li, U, L]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                    
                    # Front-facing colours are different
                    else:
                        for move in [F, U2, Fi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[47] == self.U_col:
                    
                    # Top-facing and front-facing colours are the same
                    if self.sqrs[26] == self.sqrs[48]:
                        for move in [F, U, Fi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Top-facing and front-facing colours are different
                    else:
                        for move in [Li, Ui, L]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 5:
                # White faces up
                if self.sqrs[26] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[47] == self.sqrs[50]:
                        for move in [R, Ui, Ri]: self.make_move(move)
                        # Other options: [Fi, U, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [U, Ri, F, R, Fi]: self.make_move(move)
                        # Other options: [Ui, F, Ri, Fi, R]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[33] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[47] == self.sqrs[50]:
                        for move in [U, R, U, Ri]: self.make_move(move)
                        # Other options: [U, Fi, U, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [U, Fi, Ui, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[47] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[33] == self.sqrs[34]:
                        for move in [Ui, Fi, Ui, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Ui, R, U, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 6:
                # White faces up
                if self.sqrs[26] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[33] == self.sqrs[28]:
                        for move in [Bi, R, B, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Ui, Ri, U, R]: self.make_move(move)
                        # Other options: [Ui, B, Ui, Bi]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[33] == self.U_col:
                    
                    # Front-facing and right-facing colours are the same
                    if self.sqrs[47] == self.sqrs[28]:
                        for move in [B, U, Bi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and right-facing colours are different
                    else:
                        for move in [Ri, Ui, R]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[47] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[33] == self.sqrs[28]:
                        for move in [U, B, Ui, Bi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Ri, U2, R]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 7:
                # White faces up
                if self.sqrs[26] == self.U_col:
                    
                    # Front-facing and back-facing colours are the same
                    if self.sqrs[47] == self.sqrs[3]:
                        for move in [U2, L, Ui, Li]: self.make_move(move)
                        # Other options: [U2, Bi, U, B]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and back-facing colours are different
                    else:
                        for move in [U, B, Li, Bi, L]: self.make_move(move)
                        # Other options: [Ui, Li, B, L, Bi]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[33] == self.U_col:
                    
                    # Front-facing and back-facing colours are the same
                    if self.sqrs[47] == self.sqrs[3]:
                        for move in [Ui, L, U, Li]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and back-facing colours are different
                    else:
                        for move in [Bi, U, B]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[47] == self.U_col:
                    
                    # Right-facing and left-facing colours are the same
                    if self.sqrs[33] == self.sqrs[10]:
                        for move in [U, Bi, Ui, B]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing and left-facing colours are different
                    else:
                        for move in [L, Ui, Li]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

        elif corner_node == 5:

            if edge_node == 0:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[53] == self.sqrs[46]:
                        for move in [U, R, Ui, Ri]: self.make_move(move)
                        # Other options: [U, R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [Fi, U2, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)
                
                # White faces right
                elif self.sqrs[35] == self.U_col:

                    # Front-facing colours are the same
                    if self.sqrs[53] == self.sqrs[46]:
                        for move in [U, Fi, U, F]: self.make_move(move)
                        # Other options: [Ui, R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different -> solve pair
                    elif self.sqrs[46] == self.sqrs[13]:
                        for move in [R, Li, U, L, Ri]: self.make_move(move)
                        self.F2L(permutation[1:], solved_cubes)
                    
                    # Right-facing colours are different -> don't solve pair
                    else:
                        for move in [R, U, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing and front-facing colours are the same
                    if self.sqrs[35] == self.sqrs[46]:
                        for move in [Fi, Ui, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing and front-facing colours are different
                    else:
                        self.make_move(Ui)
                        self.F2L(permutation[:], solved_cubes)
            
            elif edge_node == 1:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[35] == self.sqrs[30]:
                        for move in [Ui, Fi, U, F]: self.make_move(move)
                        # Other options: [Ui, Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [R, U2, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing and top-facing colours are the same
                    if self.sqrs[53] == self.sqrs[23]:
                        self.make_move(U)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and top-facing colours are different
                    else:
                        for move in [R, U, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[35] == self.sqrs[30]:
                        for move in [Ui, R, Ui, Ri]: self.make_move(move)
                        # Other options: [U, Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different -> solve pair
                    elif self.sqrs[30] == self.sqrs[4]:
                        for move in [Fi, B, Ui, Bi, F]: self.make_move(move)
                        self.F2L(permutation[1:], solved_cubes)

                    # Right-facing colours are different -> don't solve pair
                    else:
                        for move in [Fi, Ui, F]: self.make_move(move)
                        # Other options: [R, Ui, Ri]
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 2:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Front-facing and top-facing colours are the same
                    if self.sqrs[19] == self.sqrs[53]:
                        for move in [Fi, U, F]: self.make_move(move)
                        # Other options: [Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)
                    
                    # Front-facing and top-facing colours are different
                    else:
                        for move in [Ui, R, U, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing and top-facing colours are the same
                    if self.sqrs[19] == self.sqrs[53]:
                        self.make_move(U2)
                        self.F2L(permutation[:], solved_cubes)
                    
                    # Front-facing and top-facing colours are different
                    else:
                        for move in [R, U2, Ri]: self.make_move(move)
                        # Other options: [U, R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing and top-facing colours are the same
                    if self.sqrs[19] == self.sqrs[35]:
                        self.make_move(U)
                        self.F2L(permutation[:], solved_cubes)
                    
                    # Right-facing and top-facing colours are different
                    else:
                        for move in [R, Ui, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 3:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Front-facing and left-facing colours are the same
                    if self.sqrs[53] == self.sqrs[14]:
                        for move in [R, Ui, Ri]: self.make_move(move)
                        # Other options: [R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and left-facing colours are different
                    else:
                        for move in [U, Fi, Ui, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing and left-facing colours are the same
                    if self.sqrs[53] == self.sqrs[14]:
                        for move in [Fi, U, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and left-facing colours are different
                    else:
                        self.make_move(Ui)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing and left-facing colours are the same
                    if self.sqrs[35] == self.sqrs[14]:
                        for move in [Fi, U2, F]: self.make_move(move)
                        # Other options: [Ui, Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing and left-facing colours are different
                    else:
                        self.make_move(U2)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 4:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[48] == self.sqrs[53]:
                        for move in [Fi, U, F2, U, Fi]: self.make_move(move)
                        # Other options: [F, U, Fi, R, U, Ri], [Li, U, L, Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [Li, R, Ui, Ri, L]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[48] == self.sqrs[53]:
                        for move in [Li, Ui, L]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [F, U, Fi, Ui]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing and left-facing colours are the same
                    if self.sqrs[35] == self.sqrs[16]:
                        for move in [F, Ui, Fi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing and left-facing colours are different
                    else:
                        for move in [Li, U2, L]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 5:
                # White faces down
                if self.sqrs[42] == self.U_col:

                    # Front-facing colours are different
                    if self.sqrs[50] != self.sqrs[53]:
                        for move in [R, Ui, Ri]: self.make_move(move)
                        # Other options: [Fi, U, F]
                        self.F2L(permutation[:], solved_cubes)
                    
                    # Front-facing colours are the same -> pair already solved
                    elif self.sqrs[50] == self.sqrs[49]:
                        self.F2L(permutation[1:], solved_cubes)

                    # Front-facing colours are the same -> pair not already solved
                    else:
                        for move in [R, U, Ri]: self.make_move(move)
                        # Other options: [Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing colours are the same
                    if self.sqrs[50] == self.sqrs[53]:
                        for move in [R, Ui, Ri, Fi, U, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing colours are different
                    else:
                        for move in [R, Ui, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[34] == self.sqrs[35]:
                        for move in [Fi, U, F, R, Ui, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Fi, U, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 6:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[28] == self.sqrs[35]:
                        for move in [B, Ui, Bi, R, U, Ri]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Fi, B, U, Bi, F]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing and right-facing colours are the same
                    if self.sqrs[53] == self.sqrs[28]:
                        for move in [R, U, R2, U, R]: self.make_move(move)
                        # Other options: [Fi, Ui, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and right-facing colours are different
                    else:
                        for move in [Ri, U, R2, U, Ri]: self.make_move(move)
                        # Other options: [B, U, Bi, R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Right-facing colours are the same
                    if self.sqrs[28] == self.sqrs[35]:
                        for move in [B, U, Bi]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Right-facing colours are different
                    else:
                        for move in [Ri, U, R, Ui]: self.make_move(move)
                        # Other options: [B, Ui, Bi, Fi, U2, F]
                        self.F2L(permutation[:], solved_cubes)

            elif edge_node == 7:
                # White faces down
                if self.sqrs[42] == self.U_col:
                    
                    # Front-facing and left-facing colours are the same
                    if self.sqrs[53] == self.sqrs[10]:
                        for move in [L, R, U, Ri, Li]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and left-facing colours are different
                    else:
                        for move in [L, U, Li, Fi, Ui, F]: self.make_move(move)
                        # Other options: [Bi, Ui, B, R, U, Ri]
                        self.F2L(permutation[:], solved_cubes)

                # White faces right
                elif self.sqrs[35] == self.U_col:
                    
                    # Front-facing and left-facing colours are the same
                    if self.sqrs[53] == self.sqrs[10]:
                        for move in [R, U, Ri, L, U2, Li]: self.make_move(move)
                        # Other options: [Bi, U2, B, Fi, U, F]
                        self.F2L(permutation[:], solved_cubes)

                    # Front-facing and left-facing colours are different
                    else:
                        for move in [L, Ui, Li]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                # White faces front
                elif self.sqrs[53] == self.U_col:
                    
                    # Down-facing and left-facing colours are the same 
                    if self.sqrs[42] == self.sqrs[10]:
                        for move in [L, U2, Li]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)

                    # Down-facing and left-facing colours are different
                    else:
                        for move in [Bi, U, B]: self.make_move(move)
                        self.F2L(permutation[:], solved_cubes)


    def OLL(self):

        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col: self.rotate_cube(self.sqrs, z)

        for _ in range(4):
            dg = ['-' if self.sqrs[i] == self.D_col else ' ' for i in [6,7,8,11,14,17,27,30,33,45,46,47]]
            d01,d02,d03,d10,d20,d30,d14,d24,d34,d41,d42,d43 = dg

            dg = ['x' if self.sqrs[i] == self.D_col else 'o' for i in range(18,27)]
            d11,d12,d13,d21,d22,d23,d31,d32,d33 = dg

            diagram = (
                (' ',d01,d02,d03,' '),
                (d10,d11,d12,d13,d14),
                (d20,d21,d22,d23,d24),
                (d30,d31,d32,d33,d34),
                (' ',d41,d42,d43,' ')
            )

            if diagram in OLL_DICT: break
            else: self.rotate_cube(self.sqrs, y)
            
        for move in OLL_DICT[diagram]: self.make_move(move)


    def PLL(self):

        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col: self.rotate_cube(self.sqrs, z)

        for _ in range(4):
            labels = {self.sqrs[46]:'a', self.sqrs[30]:'b', self.sqrs[7]:'c', self.sqrs[14]:'d'}
            dg = [labels[self.sqrs[i]] for i in [6,8,11,17,27,33,45,47]]
            d01,d03,d10,d30,d14,d34,d41,d43 = dg

            diagram = (
                (' ',d01,'c',d03,' '),
                (d10,'x','x','x',d14),
                ('d','x','x','x','b'),
                (d30,'x','x','x',d34),
                (' ',d41,'a',d43,' ')
            )

            if diagram in PLL_DICT: break
            else: self.rotate_cube(self.sqrs, y)

        for move in PLL_DICT[diagram]: self.make_move(move)
        
        # Final step: turn down face
        while self.sqrs[46] != self.sqrs[49]: self.make_move(U)
