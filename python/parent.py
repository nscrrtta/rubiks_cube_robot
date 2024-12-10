from moves import Moves
from constants import *


class Parent(Moves):

    def __init__(
        self,
        squares:list[int]=[i//9 for i in range(54)],
        centers:list[int]=[0,1,2,3,4,5],
        moves:list[str]=[]):

        self.sqrs = squares
        self.moves = moves
        self.set_solved_orientation(centers)

        self.cubes_solved = 0
    

    def set_solved_orientation(self, centers:list[int]):
        
        # Final colour of each face
        self.centers = self.B_col, self.L_col, self.U_col, self.R_col, self.D_col, self.F_col = centers

        # Final position of each edge and its correct orientation
        self.solved_edges = {
            # Top layer
            0: (self.F_col, self.U_col), # FU
            1: (self.R_col, self.U_col), # RU
            2: (self.B_col, self.U_col), # BU
            3: (self.L_col, self.U_col), # LU

            # Middle layer
            4: (self.L_col, self.F_col), # LF
            5: (self.R_col, self.F_col), # RF
            6: (self.R_col, self.B_col), # RB
            7: (self.L_col, self.B_col), # LB

            # Bottom layer
            8: (self.F_col, self.D_col), # FD
            9: (self.R_col, self.D_col), # RD
            10:(self.B_col, self.D_col), # BD
            11:(self.L_col, self.D_col)  # LD
        }

        # Final positoin of each corner and its correct orientation
        self.solved_corners = {
            # Top layer
            0: (self.F_col, self.L_col, self.U_col), # FLU
            1: (self.F_col, self.R_col, self.U_col), # FRU
            2: (self.B_col, self.R_col, self.U_col), # BRU
            3: (self.B_col, self.L_col, self.U_col), # BLU

            # Bottom layer
            4: (self.F_col, self.L_col, self.D_col), # FLD
            5: (self.F_col, self.R_col, self.D_col), # FRD
            6: (self.B_col, self.R_col, self.D_col), # BRD
            7: (self.B_col, self.L_col, self.D_col)  # BLD
        }


    def get_current_edges(self, sqrs:list[int]) -> dict[int:tuple[int]]:

        return {
            # Top layer
            0: (sqrs[46], sqrs[25]), # FU
            1: (sqrs[30], sqrs[23]), # RU
            2: (sqrs[ 7], sqrs[19]), # BU
            3: (sqrs[14], sqrs[21]), # LU

            # Middle layer
            4: (sqrs[16], sqrs[48]), # LF
            5: (sqrs[34], sqrs[50]), # RF
            6: (sqrs[28], sqrs[ 5]), # RB
            7: (sqrs[10], sqrs[ 3]), # LB

            # Bottom layer
            8: (sqrs[52], sqrs[43]), # FD
            9: (sqrs[32], sqrs[39]), # RD
            10:(sqrs[ 1], sqrs[37]), # BD
            11:(sqrs[12], sqrs[41])  # LD
        }


    def get_current_corners(self, sqrs:list[int]) -> dict[int:tuple[int]]:

        return {
            # Top layer
            0: (sqrs[45], sqrs[17], sqrs[24]), # FLU
            1: (sqrs[47], sqrs[33], sqrs[26]), # FRU
            2: (sqrs[ 8], sqrs[27], sqrs[20]), # BRU
            3: (sqrs[ 6], sqrs[11], sqrs[18]), # BLU

            # Bottom layer
            4: (sqrs[51], sqrs[15], sqrs[44]), # FLD
            5: (sqrs[53], sqrs[35], sqrs[42]), # FRD
            6: (sqrs[ 2], sqrs[29], sqrs[36]), # BRD
            7: (sqrs[ 0], sqrs[ 9], sqrs[38])  # BLD
        }
    

    def get_paths(
        self,
        cubie_type:str, 
        start_node:int, 
        final_node:int, 
        move_limit:int,
        legal_moves:list[str]=[],
        illegal_moves:list[str]=[],
        solved_orientation:tuple[int]=None) -> list[list[str]]:

        all_paths = []

        def search(current_node=0, visited_nodes=[], path=[]):
            
            found_path = current_node == final_node
            
            if found_path and solved_orientation is not None:
                temp_sqrs = self.sqrs[:] # Make a copy
                for move in path: self.turn_face(temp_sqrs, move)
                if cubie_type == 'corner': d = self.get_current_corners(temp_sqrs)
                elif cubie_type == 'edge': d = self.get_current_edges(temp_sqrs)
                found_path = d[final_node] == solved_orientation
            
            if found_path:
                self.organize_moves(path)
                if path not in all_paths:
                    all_paths.append(path)
                return
            
            if len(path) >= move_limit: return

            if cubie_type == 'corner': links = CORNER_LINKS
            elif cubie_type == 'edge': links = EDGE_LINKS
            for node, set_of_moves in links[current_node].items():

                if node in visited_nodes: continue

                for move in set_of_moves:
                    if legal_moves and move not in legal_moves: continue
                    if illegal_moves and move in illegal_moves: continue
                    search(node, visited_nodes+[node], path+[move])

        search(start_node)

        # Return list of paths in order of smallest to largest
        return sorted(all_paths, key=lambda path: len(path))


    def make_move(self, move:str):

        for move in self.turn_face(self.sqrs, move):
            face, turn = move[0], move[1]

            center = {
                'B': self.sqrs[4],
                'L': self.sqrs[13],
                'U': self.sqrs[22],
                'R': self.sqrs[31],
                'D': self.sqrs[40],
                'F': self.sqrs[49] 
            }[face]

            translation = {
                self.B_col: 'B',
                self.L_col: 'L',
                self.U_col: 'U',
                self.R_col: 'R',
                self.D_col: 'D',
                self.F_col: 'F'
            }[center]

            self.moves.append(translation+turn)


    def organize_moves(self, moves:list[str], no_U=False):

        reorganize = False

        i = 0
        while i < len(moves):
            mi, ni = moves[i][0], int(moves[i][1])

            j = i+1
            while j < len(moves):
                mj, nj = moves[j][0], int(moves[j][1])

                # Same move
                if mi == mj:
                    reorganize = True
                    del moves[j]
                    ni += nj 

                # Opposite face of cube
                elif mi == OPPOSITE_FACES[mj]:
                    j += 1 

                else: break

            if ni % 4 == 0: del moves[i]
            else: moves[i] = f'{mi}{ni % 4}'; i += 1

        # If no_U is True, replace all U/U2//U' moves (because there is no U face motor)
        i = 0
        while no_U and i < len(moves):
            m, n = moves[i][0], moves[i][1]
            if m != 'U': i += 1; continue

            del moves[i]
            moves[i:i] = [L,R,F2,B2,Li,Ri,'D'+n,L,R,F2,B2,Li,Ri]

            reorganize = True

        if reorganize: self.organize_moves(moves)


    def FLD_pair_solved(self):

        f = self.sqrs[51] == self.sqrs[48] == self.sqrs[49]
        l = self.sqrs[15] == self.sqrs[16] == self.sqrs[13]
        d = self.sqrs[44] == self.sqrs[40]
        return f and l and d
    

    def FRD_pair_solved(self):

        f = self.sqrs[53] == self.sqrs[50] == self.sqrs[49]
        r = self.sqrs[35] == self.sqrs[34] == self.sqrs[31]
        d = self.sqrs[42] == self.sqrs[40]
        return f and r and d
    

    def BLD_pair_solved(self):

        b = self.sqrs[ 0] == self.sqrs[ 3] == self.sqrs[ 4]
        l = self.sqrs[ 9] == self.sqrs[10] == self.sqrs[13]
        d = self.sqrs[38] == self.sqrs[40]
        return b and l and d
    

    def BRD_pair_solved(self):

        b = self.sqrs[ 2] == self.sqrs[ 5] == self.sqrs[ 4]
        r = self.sqrs[29] == self.sqrs[28] == self.sqrs[31]
        d = self.sqrs[36] == self.sqrs[40]
        return b and r and d
    