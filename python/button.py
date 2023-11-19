from constants import png_path
import pygame


class Button:

    def __init__(self, x_pos: int, y_pos: int, png: str):

        self.x_pos  = x_pos
        self.y_pos  = y_pos
        self.width  = 52
        self.height = 52

        self.pressed_png = pygame.image.load(f'{png_path}/{png}_white.png')
        self.not_pressed_png = pygame.image.load(f'{png_path}/{png}_grey.png')

        self.pressed = False

    def clicked(self, mouse_pos: tuple) -> bool:

        x,y = mouse_pos
        self.pressed = (
            self.x_pos < x-4 < self.x_pos+self.width and 
            self.y_pos < y-4 < self.y_pos+self.height
        )
        return self.pressed
    
    def draw(self, screen):

        if self.pressed: png = self.pressed_png
        else: png = self.not_pressed_png

        screen.blit(png, (self.x_pos, self.y_pos))
