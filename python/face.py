from constants import *
import numpy as np
import pygame
import math


cubie_size = 85
delta_x = math.sqrt(3)/2
delta_y = 1/2


class Face:
    """
    This class creates a single cube face for the GUI
    The face normal is either up, right or front

    The face consists of 9 squares (that are actually rhombuses)
    the user can click to change the colours of the cube stickers
    """
    
    def __init__(self, index: int):
        """
        index:
            0 -> back face
            1 -> left face
            2 -> up face
            3 -> right face
            4 -> down face
            5 -> front face
        """

        if   index in (2,3,5): self.position = (236,285)
        elif index in (0,1,4): self.position = (787,285)

        if   index in (2,4): self.normal = 'up'
        elif index in (0,3): self.normal = 'right'
        elif index in (1,5): self.normal = 'front'

        translation_dict = {
            0: {0:0, 1:3, 2:6, 3:1, 4:4, 5:7, 6:2, 7:5, 8:8},
            1: {0:0, 1:3, 2:6, 3:1, 4:4, 5:7, 6:2, 7:5, 8:8},
            2: {0:8, 1:5, 2:2, 3:7, 4:4, 5:1, 6:6, 7:3, 8:0},
            3: {0:6, 1:7, 2:8, 3:3, 4:4, 5:5, 6:0, 7:1, 8:2},
            4: {0:2, 1:1, 2:0, 3:5, 4:4, 5:3, 6:8, 7:7, 8:6},
            5: {0:2, 1:1, 2:0, 3:5, 4:4, 5:3, 6:8, 7:7, 8:6}
        }[index]

        self.squares = {}
        
        p0 = self.get_points(self.position)
        pos = p0[0]

        i = 0
        for _ in range(3):
            for _ in range(3):
                p = self.get_points(pos)
                self.squares[ translation_dict[i] ] = p
                pos = p[-1]
                i += 1
            p0 = self.get_points(p0[1])
            pos = p0[0]

    def get_points(self, position: tuple) -> tuple:
        """
        Returns a tuple of 4 coordinates (a,b,c,d) that create a rhombus

        Face faces up:      Face faces right:     Face faces front:
              c                     b                 d
          b       d             a                         a
              a                     c                 c
                                d                         b

        <position> is the location of coordinate "a"
        """
        dx, dy = delta_x*cubie_size, delta_y*cubie_size

        b_scale = {'up':[-1,-1], 'right':[1,-1], 'front':[ 0, 2]}[self.normal]
        c_scale = {'up':[ 1,-1], 'right':[ 0,2], 'front':[-1,-1]}[self.normal]
        d_scale = {'up':[ 1, 1], 'right':[-1,1], 'front':[ 0,-2]}[self.normal]

        a = position
        b = np.add(a, np.multiply([dx, dy], b_scale))
        c = np.add(b, np.multiply([dx, dy], c_scale))
        d = np.add(c, np.multiply([dx, dy], d_scale))

        return (a,b,c,d)
    
    def get_clicked_square(self, mouse_pos: tuple) -> int:

        for i, square in self.squares.items():
            if self.square_clicked(mouse_pos, square):
                return i
        return -1

    def square_clicked(self, mouse_pos: tuple, square: tuple) -> bool:

        mx,my = mouse_pos
        q1 = q2 = q3 = q4 = False
        (ax,ay), (bx,by), (cx,cy), (dx,dy) = square

        if self.normal == 'up':
            # A to B
            x,y = ax,ay
            while x >= bx and y >= by:
                if int(y) == my and mx > x: q1 = True
                if int(x) == mx and my < y: q2 = True
                x -= delta_x; y -= delta_y
            
            # B to C
            x,y = bx,by
            while x <= cx and y >= cy:
                if int(y) == my and mx > x: q1 = True
                if int(x) == mx and my > y: q4 = True
                x += delta_x; y -= delta_y
            
            # C to D
            x,y = cx,cy
            while x <= dx and y <= dy:
                if int(y) == my and mx < x: q3 = True
                if int(x) == mx and my > y: q4 = True
                x += delta_x; y += delta_y

            # D to A
            x,y = dx,dy
            while x >= ax and y <= ay:
                if int(y) == my and mx < x: q3 = True
                if int(x) == mx and my < y: q2 = True
                x -= delta_x; y += delta_y

        elif self.normal == 'right':
            # A to B
            x,y = ax,ay
            while x <= bx and y >= by:
                if int(y) == my and mx > x: q1 = True
                if int(x) == mx and my > y: q4 = True
                x += delta_x; y -= delta_y

            # B to C
            x,y = bx,by
            while y <= cy:
                if int(y) == my and mx < x: q3 = True
                y += delta_y

            # C to D
            x,y = cx,cy
            while x >= dx and y <= dy:
                if int(y) == my and mx < x: q3 = True
                if int(x) == mx and my < y: q2 = True
                x -= delta_x; y += delta_y

            # D to A
            x,y = dx,dy
            while y >= ay:
                if int(y) == my and mx > x: q1 = True
                y -= delta_y

        elif self.normal == 'front':
            # A to B
            x,y = ax,ay
            while y <= by:
                if int(y) == my and mx < x: q3 = True
                y += delta_y

            # B to C
            x,y = bx,by
            while x >= cx and y >= cy:
                if int(y) == my and mx > x: q1 = True
                if int(x) == mx and my < y: q2 = True
                x -= delta_x; y -= delta_y

            # C to D
            x,y = cx,cy
            while y >= dy:
                if int(y) == my and mx > x: q1 = True
                y -= delta_y

            # D to A
            x,y = dx,dy
            while x <= ax and y <= ay:
                if int(y) == my and mx < x: q3 = True
                if int(x) == mx and my > y: q4 = True
                x += delta_x; y += delta_y

        return q1 == q2 == q3 == q4 == True

    def draw(self, sqrs: list, screen):
        
        for i, square in self.squares.items():
            colour = colours_rgb[ sqrs[i] ]
            pygame.draw.polygon(screen, colour, square)
            pygame.draw.polygon(screen, (50,50,50), square, width=2)
