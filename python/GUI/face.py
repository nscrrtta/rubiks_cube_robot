from .constants import FACE_1_CENTER_POS, FACE_2_CENTER_POS, RHOMBUS_SIZE, RGB_VALUES, BACKGROUND_RGB
from shapely.geometry import Point, Polygon
import numpy as np
import pygame
import math


class Face:

    def __init__(self, index: int):
        """
        index:
            0 -> Back face
            1 -> Left face
            2 -> Up face
            3 -> Right face
            4 -> Down face
            5 -> Front face
        """

        self.index = index
        
        # A GUI face consists of 9 rhombi        
        # Each rhombi is made up of 4 (x,y) coordinates, a b c d
        self.rhombi: list[tuple[int]] = []
        self.polygons: list[Polygon] = []

        dx, dy = math.sqrt(3) * RHOMBUS_SIZE / 2, RHOMBUS_SIZE / 2
        scale = np.array([dx, dy])

        center, a_coef, ab_coef, bc_coef, cd_coef = {
            0: (FACE_2_CENTER_POS, [ 0,  0], [ 0,  2], [ 1, -1], [0, -2]),
            1: (FACE_2_CENTER_POS, [ 0,  0], [-1, -1], [ 0,  2], [1,  1]),
            2: (FACE_1_CENTER_POS, [ 0, -6], [-1,  1], [ 1,  1], [1, -1]),
            3: (FACE_1_CENTER_POS, [ 3, -3], [-1,  1], [ 0,  2], [1, -1]),
            4: (FACE_2_CENTER_POS, [ 3, -3], [-1, -1], [-1,  1], [1,  1]),
            5: (FACE_1_CENTER_POS, [-3, -3], [ 0,  2], [ 1,  1], [0, -2])
        }[self.index]

        a = center + a_coef * scale
        ab, bc, cd = ab_coef * scale, bc_coef * scale, cd_coef * scale

        for _ in range(3):
            for _ in range(3):
                b = np.add(a, ab)
                c = np.add(b, bc)
                d = np.add(c, cd)

                points = (a, b, c, d)
                self.rhombi.append(points)
                self.polygons.append(Polygon(points))

                # 'a' coordinate of next rhombus
                # is 'd' coordinate of previous rhombus
                a = d
    
            # 'a' coordinate of next rhombus
            # is 'b' coordinate of first rhombus in previous row
            a = self.rhombi[-3][1]
    

    def get_clicked_rhombus(self, mouse_pos: Point) -> int:
        for i, polygon in enumerate(self.polygons):
            if mouse_pos.within(polygon):
                return i + self.index * 9


    def draw(self, squares: list[int], screen: pygame.Surface):      
        for i, rhombus in enumerate(self.rhombi):
            colour = RGB_VALUES[squares[i + self.index * 9]]
            pygame.draw.polygon(screen, colour, rhombus)
            pygame.draw.polygon(screen, BACKGROUND_RGB, rhombus, width=2)
