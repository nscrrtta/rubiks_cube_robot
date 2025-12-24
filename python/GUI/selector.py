from .constants import SELECTOR_SIZE, SELECTOR_POS, RGB_VALUES
import pygame


class Selector:

    def __init__(self, index: int):
        self.x_pos, self.y_pos = SELECTOR_POS[index]
        self.colour = RGB_VALUES[index]
        self.selected = False
        self.index = index

        self.inner_rect = self._get_rect(0)
        self.outer_rect = self._get_rect(6)


    def clicked(self, mouse_pos: tuple[int]) -> bool:
        mx, my = mouse_pos
        x = self.x_pos < mx < self.x_pos + SELECTOR_SIZE
        y = self.y_pos < my < self.y_pos + SELECTOR_SIZE
        return x and y


    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.colour, self.inner_rect, width=0, border_radius=5)
        if not self.selected: return
        pygame.draw.rect(screen, self.colour, self.outer_rect, width=2, border_radius=10)

    
    def _get_rect(self, offset: int) -> pygame.Rect:
        return pygame.Rect(
            self.x_pos - offset,
            self.y_pos - offset,
            SELECTOR_SIZE + 2 * offset,
            SELECTOR_SIZE + 2 * offset
        )
