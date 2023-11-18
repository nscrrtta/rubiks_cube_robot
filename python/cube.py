from constants import *
import move_cube


class Cube:

    def __init__(self, sqrs:list=[i//9 for i in range(54)]):

        self.sqrs   = sqrs
        self.moves  = []
        self.active = False
        self.set_centers([sqrs[9*i+4] for i in range(6)])

    def set_centers(self, centers: list):
        """
        The purpose of setting the centers of the cube
        is to note which colours each face must be
        when the cube is solved
        """
        self.B_col = centers[0]
        self.L_col = centers[1]
        self.U_col = centers[2]
        self.R_col = centers[3]
        self.D_col = centers[4]
        self.F_col = centers[5]

    def get_edges(self) -> dict:

        return {
            # Top layer
            0: tuple(self.sqrs[i] for i in [46,25]), # FU
            1: tuple(self.sqrs[i] for i in [30,23]), # RU
            2: tuple(self.sqrs[i] for i in [7, 19]), # BU
            3: tuple(self.sqrs[i] for i in [14,21]), # LU

            # Middle layer
            4: tuple(self.sqrs[i] for i in [16,48]), # LF
            5: tuple(self.sqrs[i] for i in [34,50]), # RF
            6: tuple(self.sqrs[i] for i in [28, 5]), # RB
            7: tuple(self.sqrs[i] for i in [10, 3]), # LB

            # Bottom layer
            8: tuple(self.sqrs[i] for i in [52,43]), # FD
            9: tuple(self.sqrs[i] for i in [32,39]), # RD
            10:tuple(self.sqrs[i] for i in [1, 37]), # BD
            11:tuple(self.sqrs[i] for i in [12,41])  # LD
        }

    def get_corners(self) -> dict:

        return {
            # Top layer
            0: tuple(self.sqrs[i] for i in [45,17,24]), # FLU
            1: tuple(self.sqrs[i] for i in [47,33,26]), # FRU
            2: tuple(self.sqrs[i] for i in [8 ,27,20]), # BRU
            3: tuple(self.sqrs[i] for i in [6 ,11,18]), # BLU

            # Bottom layer
            4: tuple(self.sqrs[i] for i in [51,15,44]), # FLD
            5: tuple(self.sqrs[i] for i in [53,35,42]), # FRD
            6: tuple(self.sqrs[i] for i in [2, 29,36]), # BRD
            7: tuple(self.sqrs[i] for i in [0, 9, 38])  # BRL
        }
    
    def get_paths(
        self,
        cubie_type: str, 
        start: int, 
        final: int, 
        limit: int,
        orientation=None, 
        legal_moves:list=[],
        illegal_moves:list=[]) -> list:
        """
        This function finds all unique paths that bring an edge/corner from <start> to <final> in <limit> moves or less
        The 12 edges and 8 corners of the cube are assigned an index (0,1,2...)
        See get_edges() and get_corners() for how these indices are assigned

        If <orientation> is not None, it returns all unique paths
        that bring an edge/corner from <start> to <final> in its correct orientation
            -> this is used for checking if the cube is solveable and solving the cross

        If a list of legal moves is provided, only moves in <legal_moves> are allowed
        if a list of illegal moves is provided, moves in <illegal_moves> are not allowed

        Returns: a list of all unique paths in order of smallest to largest
        """
    
        links, fnc = {
            'edge':   (edge_links,   self.get_edges  ), 
            'corner': (corner_links, self.get_corners)
        }[cubie_type]

        all_paths = []

        def search(current_node=0, visited_nodes=[], path=[]):

            valid_path = False

            if current_node == final:

                valid_path = True
                
                if orientation is not None:
                    sqrs = self.sqrs[:] 
                    for move in path: self.make_move(move,save_move=False)
                    if fnc()[final] != orientation: valid_path = False
                    self.sqrs = sqrs

            if valid_path:
                self.organize_moves(path)
                if path not in all_paths: all_paths.append(path)
                return
            
            if len(path) >= limit: return

            for node, set_of_moves in links[current_node].items():

                if node in visited_nodes: continue

                for move in set_of_moves:
                    if legal_moves and move not in legal_moves: continue
                    if illegal_moves and move in illegal_moves: continue
                    search(node, visited_nodes+[node], path+[move])

        search(start)

        # Return <all_paths> in order of smallest to largest
        return sorted(all_paths, key=lambda path: len(path))

    def make_move(self, move: str, save_move=True):
        """
        This function makes a move in code

        <move> is a two character string, where the first character is the face to be turned,
        and the second character is the number clockwise rotations (see constants.py)

        For example:
            L1 = move the left face clockwise once
            F2 = move the front face clockwise twice
            R3 = move the right face clockwise thrice (counter-clockwise once)

        If <save_move> is True, <move> is added to <self.moves> after translating it
        to later be used to turn the physical cube with the motors
        """
        m = move[0]
        n = int(move[1])

        move_set = {
        'M': move_cube.M, 'E': move_cube.E, 'S': move_cube.S,
        'F': move_cube.F, 'f': move_cube.f,
        'B': move_cube.B, 'b': move_cube.b,
        'L': move_cube.L, 'l': move_cube.l,
        'R': move_cube.R, 'r': move_cube.r,
        'U': move_cube.U, 'u': move_cube.u,
        'D': move_cube.D, 'd': move_cube.d
        }[m](self.sqrs, n)

        if save_move is False: return

        for move in move_set:
            translation = self.translate_move(move)
            self.moves.append(translation)

    def translate_move(self, move: str) -> str:
        """
        This function translates the move being made in code
        to the physical move the motors will make

        The two moves can be different if the cube was rotated in code
        For example, an L move in code could actually be an F move with the motors

        The way to determine which motor to turn
        is to note the center colour of the face being turned in code
        """
        m = move[0]
        n = int(move[1])

        center = {
            'B': self.sqrs[4],
            'L': self.sqrs[13],
            'U': self.sqrs[22],
            'R': self.sqrs[31],
            'D': self.sqrs[40],
            'F': self.sqrs[49] 
        }[m]

        translation = {
            self.B_col: 'B',
            self.L_col: 'L',
            self.U_col: 'U',
            self.R_col: 'R',
            self.D_col: 'D',
            self.F_col: 'F'
        }[center]

        return f'{translation}{n}'

    def organize_moves(self, moves: list, no_U=False):
        """
        This function combines moves of the same type if:
            1. they are made consecutively: 
                [R1, R2] -> [R3]
            2. they are separated only by moves of the opposite face:
                [R1, L1, L1, R1, R1, L1] -> [R3, L3]

        If a move is made n times and n >= 4, perform n modulo 4:
            [R1, R2, R3] -> [R6] -> [R2]

        Example: moves = [R1, L1, L1, L1, R1, L1, L1, U2, D, U2, D3, L1, L1, L1]
        result: [R2]    

        It will recursively organize <moves> until there is nothing more that can be done    
        """

        reorganize = False

        i = 0
        while i < len(moves):

            mi = moves[i][0]
            ni = int(moves[i][1])

            j = i+1
            while j < len(moves):

                mj = moves[j][0]
                nj = int(moves[j][1])

                # Same move
                if mi == mj:
                    reorganize = True
                    del moves[j]
                    ni += nj 

                # Opposite face of cube
                elif mi == opposite_faces[mj]:
                    j += 1 

                else: break

            if ni%4 == 0: del moves[i]
            else: moves[i] = f'{mi}{ni%4}'; i += 1

        # If no_U is True, replace all U/U2//U' moves (because there is no U face motor)
        i = 0
        while no_U and i < len(moves):

            X = defaultdict(lambda: False, {U:D, Ui:Di, U2:D2})[moves[i]]
            if X is False: i += 1; continue

            del moves[i]
            for move in [L,R,F2,B2,Li,Ri,X,L,R,F2,B2,Li,Ri][::-1]:
                moves.insert(i, move)

            reorganize = True

        if reorganize: self.organize_moves(moves)

    ###########################
    #   STEPS TO SOLVE CUBE   #
    ###########################

    def solveable(self) -> bool:

        # The home position of each edge and its correct orientation
        edges = {
            0: (self.F_col, self.U_col), 1: (self.R_col, self.U_col), 2: (self.B_col, self.U_col), 3: (self.L_col, self.U_col),
            4: (self.L_col, self.F_col), 5: (self.R_col, self.F_col), 6: (self.R_col, self.B_col), 7: (self.L_col, self.B_col),
            8: (self.F_col, self.D_col), 9: (self.R_col, self.D_col), 10:(self.B_col, self.D_col), 11:(self.L_col, self.D_col)
        }

        # The home positoin of each corner and its correct orientation
        corners = {
            0: (self.F_col, self.L_col, self.U_col), 1: (self.F_col, self.R_col, self.U_col),
            2: (self.B_col, self.R_col, self.U_col), 3: (self.B_col, self.L_col, self.U_col),
            4: (self.F_col, self.L_col, self.D_col), 5: (self.F_col, self.R_col, self.D_col),
            6: (self.B_col, self.R_col, self.D_col), 7: (self.B_col, self.L_col, self.D_col)
        }

        def illegal_stickers() -> bool:
            """
            Returns True if the stickers on the cube are placed
            in a way that makes the cube impossible to solve
            """

            # Must be exactly 9 stickers of each colour
            for i in range(6):
                if self.sqrs.count(i) != 9: return True

            # All edges/corners must be solveable, meaning there exists a path 
            # that returns it to its home position in its correct orientation
            for d1, d2, cubie_type in [(edges, self.get_edges(), 'edge'), (corners, self.get_corners(), 'corner')]:
                for i, cubie1 in d1.items():
                    for j, cubie2 in d2.items():
                        if set(cubie1).issubset(set(cubie2)): break

                    # No paths exist: edge/corner is not solveable
                    if not self.get_paths(cubie_type,j,i,3,cubie1): return True

            return False

        def count_swaps() -> int:
            """
            Counts the number of corners that were swapped
            and the number of edges that were swapped

            Returns the sum <num_swaps>
            """

            num_swaps = 0

            for d1, d2 in [(edges, self.get_edges()), (corners, self.get_corners())]:

                swap_dict = {}
                
                for i, cubie1 in d1.items():
                    for j, cubie2 in d2.items():
                        if set(cubie1).issubset(set(cubie2)):
                            swap_dict[i] = j; break
                        
                while True:
                    for key, val in swap_dict.items():
                        if key == val: continue
                        swap_dict[key],swap_dict[val] = swap_dict[val], swap_dict[key]
                        num_swaps += 1
                        break
                    else: break

            return num_swaps

        def count_flipped_edges() -> int:
            """
            Bring each edge to its home position without using any F/Fi/B/Bi moves
            then check if the edge as been flipped

            Returns the sum <flipped_edges>
            """

            flipped_edges = 0

            for i, edge1 in edges.items():

                # Locate position of edge
                for j, edge2 in self.get_edges().items():
                    if set(edge1).issubset(set(edge2)): break
                
                # Find paths that returns edge to home position in its correct orientation
                # If no paths exist, the edge is flipped
                if not self.get_paths('edge',j,i,2,edge1,illegal_moves=[F,Fi,B,Bi]):
                    flipped_edges += 1 

            return flipped_edges

        def count_sum_of_corners() -> int:
            """
            For all 8 corners, check if they've been flipped clockwise, counter-clockwise, or not at all
            Corners flipped clockwise are assigned a value of 1
            Corners flipped counter-clockwise are assigned a value of 2
            
            Returns the sum of all 8 corners <sum>
            """

            sum = 0
            top = self.sqrs[22] # Colour of top face
            bot = self.sqrs[40] # Colour of bottom face

            # Rotate cube 4 times. look at FRU and FRD corners
            for _ in range(4):
                if self.sqrs[33] in [top, bot]: sum += 1
                if self.sqrs[47] in [top, bot]: sum += 2
                if self.sqrs[53] in [top, bot]: sum += 1
                if self.sqrs[35] in [top, bot]: sum += 2
                move_cube.rotate_cube(self.sqrs, y)

            return sum
        
        # No illegal stickers
        if illegal_stickers(): return False

        # Number of swaps must be even
        if count_swaps() % 2 != 0: return False

        # Number of flipped edges must be even
        if count_flipped_edges() % 2 != 0: return False

        # Sum of all corners must be a multiple of 3
        if count_sum_of_corners() % 3 != 0: return False

        # Cube is solveable
        return True
    
    def cross(self, edges: list, cubes: dict):
        """
        This function solves the cross by solving one edge at a time
        <edges> (a list of integers) is the order in which the edges are solved

        ex: edges = [5, 3, 0, 1] = [front, right, back, left]

        For each edge, it finds all paths that solve the edge
        and will recursively continue down each path

        This is probably not the smartest way to solve the cross,
        but it's the best method I could come up with
        """

        # No more edges left to solve
        if len(edges) == 0:
            self.organize_moves(self.moves, no_U=True)
            cubes[tuple(self.moves)] = (tuple(self.sqrs))
            return
        
        # Edge at the front of the list is the one we're solving
        edge = (edges[0], self.U_col)

        # Rotate cube so home position of edge is FU (index 0)
        while self.sqrs[49] != edge[0]:
            move_cube.rotate_cube(self.sqrs, y)

        # Find where on the cube the edge is located
        for i, edge1 in self.get_edges().items():
            if set(edge).issubset(set(edge1)): break

        # Check which edges of the cross are already solved
        # and avoid moves that would unsolve those edges
        solved_edges  = [
            (self.sqrs[31],self.sqrs[23]) == (self.sqrs[30],self.sqrs[22]), # right
            (self.sqrs[4], self.sqrs[19]) == (self.sqrs[7], self.sqrs[22]), # back
            (self.sqrs[13],self.sqrs[21]) == (self.sqrs[14],self.sqrs[22])  # left
        ]

        illegal_moves = []
        for j, moves in enumerate(([R,R2,Ri],[B,B2,Bi],[L,L2,Li])):
            if solved_edges[j]: illegal_moves += moves
        if any(solved_edges): illegal_moves += [U,U2,Ui]

        for j in range(2,5): # limits
            # Get the smallest unique paths that solve this edge
            # without unsolving any other edges in the cross
            paths = self.get_paths('edge',i,0,j,edge,illegal_moves=illegal_moves)
            if paths: break
        else:
            # No paths of length <= 4 found
            # some paths are impossible with certain illegal moves
            # ex: if edge is in position 0 and flipped, it cannot be solved without moving L/R
            illegal_moves = [B2] + ( [B,Bi] if 9<=i<=11 else [] )
            paths = self.get_paths('edge',i,0,3,edge,illegal_moves=illegal_moves)

            # Fix paths so cross is maintained
            for path in paths:

                # Paths that end in F,F2,Fi
                if path[-1] in [F,F2,Fi]:
                    if len(path) > 2 and 0<=i<=7:
                        move  = path[-3]
                        index = -1
                    else:
                        move  = path[-2]
                        index = len(path)

                # Paths that end in U,U2,Ui
                elif path[-1] in [U,U2,Ui]:
                    move  = path[-1]
                    index = -2

                m,n = move[0], int(move[1])
                path.insert(index, f'{m}{4-n}')

        # Explore all the paths
        for path in paths:

            sqrs  = self.sqrs[:]
            moves = self.moves[:]

            for move in path: self.make_move(move)
            self.cross(edges[1:], cubes)

            self.sqrs  = sqrs
            self.moves = moves

    def F2L  (self, pairs: list, cubes: dict):
        """
        This function solves the first two layers by solving one pair at a time
        <pairs> (a list of tuples) is the order in which the pairs are solved

        ex: pairs = [(5,1), (3,5), (0,3), (1,0)]
        = (front,left), (right,front), (back,right), (left,back)

        The first integer in pair is always the front face,
        and the second integer is always the left face

        A pair is ready to be solved if:
            the edge and corner are on top
            the edge and corner are in their slot
            the edge/corner is on top and the corner/edge is in its slot
        Otherwise:
            this function recursively explores each way
            to bring the edge/corner to the top,
            then solves the pair

        Again, this is probably not the smartest way to solve the first two layers,
        but it's the best method I could come up with
        """

        # No more pairs left to solve
        if len(pairs) == 0:
            self.organize_moves(self.moves, no_U=True)
            cubes[tuple(self.moves)] = (tuple(self.sqrs))
            return

        p1,p2 = pairs[0] # front, right

        def solve_pair(e: int, c: int):

            labels = {p1:'a', p2:'b', self.U_col:'x'}

            # Corner on top
            if 0 <= c <= 3:
                # Bring corner to position 1 (FRU)
                moves = self.get_paths('corner',c,1,1,legal_moves=[U,U2,Ui])[0]
                for move in moves: self.make_move(move)

                # Relocate edge
                for e, edge in self.get_edges().items():
                    if {p1,p2}.issubset(set(edge)): break

                # Edge on top
                if 0 <= e <= 3:
                    diagram = [' ' for _ in range(16)]
                    
                    for i in [0,1,2,4,5,6,8,9,10]: diagram[i] = '-'
                    diagram[ {0:9, 1:6, 2:1, 3:4}[e] ] = labels[ self.sqrs[ {0:25, 1:23, 2:19, 3:21}[e] ] ]

                    for key, val in {
                    7:31,10:26,11:33,13:49,14:47,
                    }.items(): diagram[key] = labels[ self.sqrs[val] ]

                    diagram = [diagram[4*i:4*(i+1)] for i in range(4)]
                    diagram = tuple([tuple(row) for row in diagram])

                    moves = F2L_dict_A[diagram]
                    for move in moves: self.make_move(move)

                # Edge in slot
                else:
                    diagram = [' ' for _ in range(4)]

                    for key, val in {
                    0:47, 1:33, 2:50, 3:34
                    }.items(): diagram[key] = labels[ self.sqrs[val] ]                         

                    diagram = [diagram[2*i:2*(i+1)] for i in range(2)]
                    diagram = tuple([tuple(row) for row in diagram])

                    moves = F2L_dict_B[diagram]
                    for move in moves: self.make_move(move)

            # Edge on top, corner in slot
            elif 0 <= e <= 3:
                # Bring edge to home position
                home = 0 if self.get_edges()[e] == (p1,p2) else 1

                moves = self.get_paths('edge',e,home,1,legal_moves=[U,U2,Ui])[0]
                for move in moves: self.make_move(move)

                diagram = []
                for val in [53,35]: diagram.append( labels[ self.sqrs[val] ] )
                diagram = (home, tuple(diagram))

                moves = F2L_dict_C[diagram]
                for move in moves: self.make_move(move)

            # Corner and edge in slot
            else:
                diagram = [' ' for _ in range(4)]

                for key, val in {
                0:50, 1:34, 2:53, 3:35
                }.items(): diagram[key] = labels[ self.sqrs[val] ]

                diagram = [diagram[2*i:2*(i+1)] for i in range(2)]
                diagram = tuple([tuple(row) for row in diagram])

                moves = F2L_dict_D[diagram]
                for move in moves: self.make_move(move)

        edge_ready = corner_ready = False

        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col:
            move_cube.rotate_cube(self.sqrs, z)
        
        # Rotate cube until p1 face is in front and p2 face is on right
        while not (self.sqrs[49]==p1 and self.sqrs[31]==p2):
            move_cube.rotate_cube(self.sqrs, y)

        # Locate edge and corner
        for e, edge in self.get_edges().items():
            if {p1,p2}.issubset(set(edge)): break
        for c, corner in self.get_corners().items():
            if {p1,p2,self.U_col}.issubset(set(corner)): break


        # Edge not on top or in slot
        if not (0<=e<=3 or e==5):

            # Rotate cube until edge is in position 5 (RF)
            while not {p1,p2}.issubset( set( self.get_edges()[5] ) ):
                move_cube.rotate_cube(self.sqrs, y)

            # Relocate position of corner
            for c, corner in self.get_corners().items():
                if {p1,p2,self.U_col}.issubset(set(corner)): break

            # There are 4 ways to bring the edge to the top face without affecting other slots
            # Some ways are better than others depending on the location of the corner
            if   c == 1: options = [[R,Ui,Ri], [Fi,U,F ]]
            elif c == 2: options = [[R,U, Ri], [R,Ui,Ri], [Fi,Ui,F]]
            elif c == 0: options = [[R,U, Ri], [Fi,U,F ], [Fi,Ui,F]]
            else: options = [[R,U,Ri], [R,Ui,Ri], [Fi,U,F], [Fi,Ui,F]]
            
            # Explore all options
            for option in options:

                sqrs  = self.sqrs[:]
                moves = self.moves[:]

                for move in option: self.make_move(move)
                self.F2L(pairs[:], cubes)

                self.sqrs  = sqrs[:]
                self.moves = moves[:]

        else: edge_ready = True

        # Corner not on top or in slot
        if not (0<=c<=3 or c==5):

            # Rotate cube until corner is in position 5 (FRD)
            while not {p1,p2,self.U_col}.issubset( set( self.get_corners()[5] ) ):
                move_cube.rotate_cube(self.sqrs, y)

            # Relocate position of edge
            for e, edge in self.get_edges().items():
                if {p1,p2}.issubset(set(edge)): break
            
            # There are 4 ways to bring the corner to the top face without affecting other slots
            # Some ways are better than others depending on the location of the edge
            if   e == 0: options = [[R,U,Ri], [Fi,U,F ], [Fi,Ui,F]]
            elif e == 1: options = [[R,U,Ri], [R,Ui,Ri], [Fi,Ui,F]]
            elif e == 2: options = [[Fi,U,F], [R,Ui,Ri], [Fi,Ui,F]]
            elif e == 3: options = [[R,U,Ri], [R,Ui,Ri], [Fi,U, F]]
            else: options = [[R,U,Ri], [R,Ui,Ri], [Fi,U,F], [Fi,Ui,F]]

            # Explore all options
            for option in options:

                sqrs  = self.sqrs[:]
                moves = self.moves[:]

                for move in option: self.make_move(move)
                self.F2L(pairs[:], cubes)

                self.sqrs  = sqrs
                self.moves = moves
            
        else: corner_ready = True

        if edge_ready and corner_ready:
            solve_pair(e,c)
            self.F2L(pairs[1:], cubes)

    def OLL(self):

        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col:
            move_cube.rotate_cube(self.sqrs, z)

        moves = False

        # Rotate cube until we obtain one of the 58 scenarios
        while moves is False:
            """
            <diagram> is a 5x5 tuple of strings representing the position we see when looking down on the top layer
            x's and o's make up the 9 squares facing up, 
            where an x represents a square that belongs in the top layer
            a '-' represents a square facing front/back/left/right that belongs in the top layer
            
            Example: cross with two headlights

            (   -   -   )
            (   o x o   )
            (   x x x   )
            (   o x o   )
            (   -   -   )

            Rotate the cube until we have a diagram from OLL_dict in constants.py
            """
            move_cube.rotate_cube(self.sqrs, y)

            diagram = [' ' for _ in range(25)]

            for key, val in {
            6:18, 7:19, 8:20, 11:21, 12:22, 13:23, 16:24, 17:25, 18:26
            }.items(): diagram[key] = 'x' if self.sqrs[val] == self.D_col else 'o'
            
            for key, val in {
            1:6, 2:7, 3:8, 5:11, 9:27, 10:14, 14:30, 15:17, 19:33, 21:45, 22: 46, 23:47
            }.items(): diagram[key] = '-' if self.sqrs[val] == self.D_col else ' '

            diagram = [diagram[5*i:5*(i+1)] for i in range(5)]
            diagram = tuple([tuple(row) for row in diagram])

            moves = OLL_dict[diagram]

        for move in moves: self.make_move(move)

    def PLL(self):

        # Make sure cube is up-side-down
        while self.sqrs[22] != self.D_col:
            move_cube.rotate_cube(self.sqrs, z)

        moves = False

        # Rotate cube until we obtain one of the 22 scenarios
        while moves is False:
            """
            <diagram> is a 5x5 tuple of strings representing the position we see when looking down on the top layer
            a's, b's, c's, and d's make up the 12 squares in the top layer facing front/back/left/right
            x's make up the 9 squares facing up
            Each letter represents a colour
            
            Example:

            (   a b a   )
            ( c x x x d )
            ( d x x x c )
            ( c x x x d )
            (   b a b   )

            Rotate the cube until we have a diagram from OLL_dict in constants.py
            """

            move_cube.rotate_cube(self.sqrs, y)

            diagram = [' ' for _ in range(25)]

            labels = {
                self.sqrs[46]: 'a',
                self.sqrs[30]: 'b',
                self.sqrs[7 ]: 'c',
                self.sqrs[14]: 'd'
            }

            for key in [6,7,8,11,12,13,16,17,18]: diagram[key] = 'x'

            for key, val in {
            1:6, 2:7, 3:8, 5:11, 9:27, 10:14, 14:30, 15:17, 19:33, 21:45, 22: 46, 23:47
            }.items(): diagram[key] = labels[ self.sqrs[val] ]

            diagram = [diagram[5*i:5*(i+1)] for i in range(5)]
            diagram = tuple([tuple(row) for row in diagram])

            moves = PLL_dict[diagram]
        
        for move in moves: self.make_move(move)
        
        # Final step
        while self.sqrs[46] != self.sqrs[49]: self.make_move(U)
