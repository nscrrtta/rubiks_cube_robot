from constants import *
import pygame


# screen x,y coordinates of boxes
box_pos = {
    5: (417, 35), # Red
    2: (484, 35), # White
    3: (551, 35), # Blue

    1: (417, 480), # Green
    4: (484, 480), # Yellow
    0: (551, 480), # Orange
}


class Box:

    def __init__(self, index: int):

        self.index = index

        self.x, self.y = box_pos[index]
        self.colour = colours_rgb[index]

        self.size = 56
        self.selected = False

    def clicked(self, mouse_pos: tuple) -> bool:

        x, y = mouse_pos
        return self.x < x < self.x+self.size and self.y < y < self.y+self.size
    
    def draw(self, screen):

        if self.selected:
            rect = pygame.Rect(self.x-6, self.y-6, self.size+12, self.size+12)
            pygame.draw.rect(screen, self.colour, rect, width=2, border_radius=10)

        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.colour, rect, border_radius=5)
