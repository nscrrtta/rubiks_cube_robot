from shapely.geometry import Point

from .constants import *
from .selector import Selector
from .button import Button
from .face import Face

from Cube.solveable import Solveable
from Cube.cube import Cube
import pygame
import os


class GUI:

    def __init__(self, cube: Cube):
        self.cube = cube
        self.solveable = Solveable(cube)

        # Load window at top-left corner of screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        pygame.display.set_caption("Rubik's Cube Robot by Nick Sciarretta")

        self.faces = [Face(i) for i in range(6)]
        self.selectors = [Selector(i) for i in range(6)]

        self.selected_col = self.selectors[5] # Red selected by default
        self.selected_col.selected = True

        self.solve_btn = Button(SOLVE_BUTTON_POS, 'solve')
        self.scrmb_btn = Button(SCRMB_BUTTON_POS, 'scrmb')
        self.abort_btn = Button(ABORT_BUTTON_POS, 'abort')
        self.abort_btn.enabled = False

        self.FRU_IMG = pygame.image.load(f'./png/FRU.png')
        self.BLD_IMG = pygame.image.load(f'./png/LBD.png')

        self.font = pygame.font.SysFont('Arial', 30)
        self.num_moves = self.show_num_moves = 0
        

    def handle_mouse_click(self, mouse_pos: tuple[int], motors_busy: bool) -> bool:
        # Abort button
        if self.abort_btn.enabled and self.abort_btn.clicked(mouse_pos):
            self.abort_btn.enabled = False
            self.abort_btn.pressed = True
            return True
        
        # When motors are turning, only abort button can be pressed
        if motors_busy: return False

        # Solve and Scramble buttons
        for btn in [self.solve_btn, self.scrmb_btn]:
            if btn.enabled and btn.clicked(mouse_pos):
                self.show_num_moves = btn == self.solve_btn
                self.num_moves = 0

                self.solve_btn.enabled = False
                self.scrmb_btn.enabled = False
                self.abort_btn.enabled = True
                
                btn.pressed = True
                return True
        
        # Changing selected colour
        for selector in self.selectors:
            if selector.clicked(mouse_pos):
                self.selected_col.selected = False
                self.selected_col = selector
                selector.selected = True
                return True

        # Changing colour of rhombus
        point = Point(mouse_pos)
        for face in self.faces:
            i = face.get_clicked_rhombus(point)
            if i is None: continue
            self.cube.squares[i] = self.selected_col.index

            # If changed colour of center piece
            if i % 9 == 4:
                self.cube.centers[i//9] = self.selected_col.index

            # Check if cube is solveable
            self.solve_btn.enabled = \
            self.scrmb_btn.enabled = \
            self.solveable.is_solveable()
            return True
        
        return False


    def reset_buttons(self):
        self.solve_btn.enabled = True
        self.scrmb_btn.enabled = True
        self.abort_btn.enabled = False

    
    def increment_num_moves(self):
        self.num_moves += 1
        self.text_surface = self.font.render(f'{self.num_moves}', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=NUMBER_POS)


    def draw(self):
        self.screen.fill(BACKGROUND_RGB)

        for face in self.faces:
            face.draw(self.cube.squares, self.screen)
            
        for col_selector in self.selectors:
            col_selector.draw(self.screen)

        for btn in [self.solve_btn, self.scrmb_btn, self.abort_btn]:
            btn.draw(self.screen)

        self.screen.blit(self.FRU_IMG, FRU_IMG_POS)
        self.screen.blit(self.BLD_IMG, BLD_IMG_POS)

        if self.num_moves > 0 and self.show_num_moves:
            self.screen.blit(self.text_surface, self.text_rect)

        pygame.display.update()
