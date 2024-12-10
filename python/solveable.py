from parent import Parent
from constants import *


class Solveable(Parent):

    def is_solveable(self) -> bool:

        # Must be exactly 9 stickers of each colour
        for i in range(6):
            if self.sqrs.count(i) != 9:
                return False

        # Determine final colour of each face
        centers = [self.sqrs[i*9 + 4] for i in range(6)]
        self.set_solved_orientation(centers)

        # No illegal stickers
        if not self.legal_stickers(): return False

        # Number of swaps must be even
        if self.get_num_swaps() % 2 != 0: return False

        # Number of flipped edges must be even
        if self.get_num_flipped_edges() % 2 != 0: return False

        # Sum of all corners must be a multiple of 3
        if self.get_sum_corners() % 3 != 0: return False

        # Cube is solveable
        return True


    def legal_stickers(self) -> bool:

        # All edges/corners must be solveable, meaning there exists a path 
        # that returns it to its home position in its correct orientation
        
        for final_node, solved_edge in self.solved_edges.items():
            # Locate edge
            for start_node, current_edge in self.get_current_edges(self.sqrs).items():
                if set(solved_edge).issubset(set(current_edge)): break

            # If no paths exist, edge is not solveable
            if self.get_paths('edge',start_node,final_node,3,[],[],solved_edge) == []:
                return False
            
        for final_node, solved_corner in self.solved_corners.items():
            # Locate corner
            for start_node, current_corner in self.get_current_corners(self.sqrs).items():
                if set(solved_corner).issubset(set(current_corner)): break

            # If no paths exist, corner is not solveable
            if self.get_paths('corner',start_node,final_node,3,[],[],solved_corner) == []:
                return False
            
        # All edges/corners are solveable
        return True


    def get_num_swaps(self) -> int:

        num_swaps = 0

        # Count swapped edges
        swap_dict = {}
        for i, solved_edge in self.solved_edges.items():
            for j, current_edge in self.get_current_edges(self.sqrs).items():
                if set(solved_edge).issubset(set(current_edge)):
                    swap_dict[i] = j; break
        
        while True:
            for key, val in swap_dict.items():
                if key == val: continue
                swap_dict[key],swap_dict[val] = swap_dict[val],swap_dict[key]
                num_swaps += 1
                break
            else: break

        # Count swapped corners
        swap_dict = {}
        for i, solved_corner in self.solved_corners.items():
            for j, current_corner in self.get_current_corners(self.sqrs).items():
                if set(solved_corner).issubset(set(current_corner)):
                    swap_dict[i] = j; break
                
        while True:
            for key, val in swap_dict.items():
                if key == val: continue
                swap_dict[key],swap_dict[val] = swap_dict[val],swap_dict[key]
                num_swaps += 1
                break
            else: break

        return num_swaps


    def get_num_flipped_edges(self) -> int:

        flipped_edges = 0

        for final_node, solved_edge in self.solved_edges.items():
            # Locate edge
            for start_node, current_edge in self.get_current_edges(self.sqrs).items():
                if set(solved_edge).issubset(set(current_edge)): break
            
            # If unable to solve edge without using F, F', B, or B' moves, edge is flipped
            if self.get_paths('edge',start_node,final_node,2,[],[F,Fi,B,Bi],solved_edge) == []:
                flipped_edges += 1 

        return flipped_edges


    def get_sum_corners(self) -> int:

        sum = 0

        # Rotate cube 4 times. look at FRU and FRD corners
        for _ in range(4):
            if self.sqrs[33] in [self.U_col, self.D_col]: sum += 1
            if self.sqrs[47] in [self.U_col, self.D_col]: sum += 2
            if self.sqrs[53] in [self.U_col, self.D_col]: sum += 1
            if self.sqrs[35] in [self.U_col, self.D_col]: sum += 2
            self.rotate_cube(self.sqrs, y)
        
        return sum
