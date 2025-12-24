from .constants import BUTTON_SIZE
import pygame


class Button:

    def __init__(self, position: tuple[int], name: str):
        self.x_pos, self.y_pos = position

        self.enabled_img = pygame.image.load(f'./png/{name}_white.png')
        self.disabled_img = pygame.image.load(f'./png/{name}_grey.png')

        self.enabled = True # Can only press button when self.enabled = True
        self.pressed = False


    def clicked(self, mouse_pos: tuple[int]) -> bool:
        mx, my = mouse_pos
        x = self.x_pos < mx - 4 < self.x_pos + BUTTON_SIZE
        y = self.y_pos < my - 4 < self.y_pos + BUTTON_SIZE
        return x and y
    
    
    def draw(self, screen: pygame.Surface):
        if self.enabled: img = self.enabled_img
        else: img = self.disabled_img
        screen.blit(img, (self.x_pos, self.y_pos))
