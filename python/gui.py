from shapely.geometry import Point, Polygon
from constants import *
from cube import Cube
import numpy as np
import pygame
import math
import os


class GUI:

    def __init__(self):
        # Load window at top-left corner of screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        pygame.display.set_caption("Rubik's Cube Robot by Nick Sciarretta")

        self.faces = [Face(i) for i in range(6)]
        self.col_selectors = [ColourSelector(i) for i in range(6)]

        self.selected_col = self.col_selectors[5] # Red selected by default
        self.selected_col.selected = True

        self.solve_btn = Button(SOLVE_BUTTON_XY, 'solve')
        self.scrmb_btn = Button(SCRMB_BUTTON_XY, 'scrmb')
        self.abort_btn = Button(ABORT_BUTTON_XY, 'abort')
        self.abort_btn.enabled = False

        self.FRU_PNG_XY = pygame.image.load(f'{PNG_PATH}/FRU.png')
        self.LBD_PNG_XY = pygame.image.load(f'{PNG_PATH}/LBD.png')

        self.cube = Cube()
        

    def handle_mouse_click(self, mouse_pos:tuple[int], motors_busy:bool):

        # Abort button
        if self.abort_btn.enabled and self.abort_btn.clicked(mouse_pos):
            self.abort_btn.enabled = False
            self.abort_btn.pressed = True
            return
        
        # When motors are turning, only abort button can be pressed
        if motors_busy: return

        # Solve button
        if self.solve_btn.enabled and self.solve_btn.clicked(mouse_pos):
            self.solve_btn.enabled = False
            self.scrmb_btn.enabled = False
            self.abort_btn.enabled = True
            self.solve_btn.pressed = True
            return
        
        # Scramble button
        if self.scrmb_btn.enabled and self.scrmb_btn.clicked(mouse_pos):
            self.solve_btn.enabled = False
            self.scrmb_btn.enabled = False
            self.abort_btn.enabled = True
            self.scrmb_btn.pressed = True
            return

        # Changing colour of rhombus
        for face in self.faces:
            i = face.get_clicked_rhombus(mouse_pos)
            if i is not None:
                self.cube.sqrs[i] = self.selected_col.index

                # User updated colour -> check if cube is solveable
                solveable = self.cube.is_solveable()
                self.solve_btn.enabled = solveable
                self.scrmb_btn.enabled = solveable
                return

        # Changing selected colour
        for col_selector in self.col_selectors:
            if col_selector.clicked(mouse_pos):
                self.selected_col.selected = False
                self.selected_col = col_selector
                col_selector.selected = True
                return
            
    
    def reset_buttons(self):
        self.solve_btn.enabled = True
        self.scrmb_btn.enabled = True
        self.abort_btn.enabled = False
        

    def draw(self):
        self.screen.fill(BACKGROUND_RGB)

        for face in self.faces: face.draw(self.cube.sqrs, self.screen)
        for col_selector in self.col_selectors: col_selector.draw(self.screen)
        for btn in [self.solve_btn, self.scrmb_btn, self.abort_btn]: btn.draw(self.screen)

        self.screen.blit(self.FRU_PNG_XY, FRU_PNG_XY)
        self.screen.blit(self.LBD_PNG_XY, LBD_PNG_XY)

        pygame.display.update()


class Face:

    def __init__(self, index:int):
        """
        index {0, 1, 2, 3, 4, 5}:
            0 -> Back face
            1 -> Left face
            2 -> Up face
            3 -> Right face
            4 -> Down face
            5 -> Front face
        """

        self.index = index
        self.rhombi = []

        """        
        A GUI face consists of 9 rhombi        
        Each rhombi is made up of 4 (x,y) coordinates, a b c d
        """

        dx, dy = math.sqrt(3)*RHOMBUS_SIZE/2, RHOMBUS_SIZE/2

        if self.index == 0: # Back face
            a = RIGHT_CENTER_XY
            a_to_b, b_to_c, c_to_d = [0,2*dy], [dx,-dy], [0,-2*dy]
        
        elif self.index == 1: # Left face
            a = RIGHT_CENTER_XY
            a_to_b, b_to_c, c_to_d = [-dx,-dy], [0,2*dy], [dx,dy]
        
        elif self.index == 2: # Top face
            a = np.add(LEFT_CENTER_XY, [0,-6*dy])
            a_to_b, b_to_c, c_to_d = [-dx,dy], [dx,dy], [dx,-dy]
        
        elif self.index == 3: # Right face
            a = np.add(LEFT_CENTER_XY, [3*dx,-3*dy])
            a_to_b, b_to_c, c_to_d = [-dx,dy], [0,2*dy], [dx,-dy]
        
        elif self.index == 4: # Down face
            a = np.add(RIGHT_CENTER_XY, [3*dx,-3*dy])
            a_to_b, b_to_c, c_to_d = [-dx,-dy], [-dx,dy], [dx,dy]
        
        elif self.index == 5: # Front face
            a = np.add(LEFT_CENTER_XY, [-3*dx,-3*dy])
            a_to_b, b_to_c, c_to_d = [0,2*dy], [dx,dy], [0,-2*dy]

        for _ in range(3):
            for _ in range(3):
                b = np.add(a, a_to_b)
                c = np.add(b, b_to_c)
                d = np.add(c, c_to_d)

                self.rhombi.append((a,b,c,d))

                # 'a' coordinate of next rhombus
                # is 'd' coordinate of previous rhombus
                a = d
    
            # 'a' coordinate of next rhombus
            # is 'b' coordinate of first rhombus in previous row
            a = self.rhombi[-3][1]
    

    def get_clicked_rhombus(self, mouse_pos:tuple[int]) -> int:
        """
        Returns None if no rhombus was clicked
        """

        for i, rhombus in enumerate(self.rhombi):
            if Point(mouse_pos).within(Polygon(rhombus)):
                return i + self.index*9


    def draw(self, sqrs:list[int], screen):      
        for i, rhombus in enumerate(self.rhombi):
            colour = RGB_VALUES[sqrs[i + self.index*9]]
            pygame.draw.polygon(screen, colour, rhombus)
            pygame.draw.polygon(screen, BACKGROUND_RGB, rhombus, width=2)


class ColourSelector:

    def __init__(self, index:int):
        """
        index {0, 1, 2, 3, 4, 5}:
            0 -> Orange
            1 -> Green
            2 -> White
            3 -> Blue
            4 -> Yellow
            5 -> Red
        """

        self.x, self.y = COLOUR_SELECTOR_XY[index]
        self.colour = RGB_VALUES[index]
        self.selected = False
        self.index = index


    def clicked(self, mouse_pos:tuple[int]) -> bool:
        x,y = mouse_pos
        return (
            self.x < x < self.x+COLOUR_SELECTOR_SIZE and 
            self.y < y < self.y+COLOUR_SELECTOR_SIZE
        )


    def draw(self, screen):
        # Draw box
        rect = pygame.Rect(self.x, self.y, COLOUR_SELECTOR_SIZE, COLOUR_SELECTOR_SIZE)
        pygame.draw.rect(screen, self.colour, rect, border_radius=5)

        if self.selected:
            # Draw a border around box
            rect = pygame.Rect(self.x-6, self.y-6, COLOUR_SELECTOR_SIZE+12, COLOUR_SELECTOR_SIZE+12)
            pygame.draw.rect(screen, self.colour, rect, width=2, border_radius=10)


class Button:

    def __init__(self, coordinate:tuple[int], name:str):
        self.x_coor, self.y_coor = coordinate

        self.pressed_png = pygame.image.load(f'{PNG_PATH}/{name}_white.png')
        self.not_pressed_png = pygame.image.load(f'{PNG_PATH}/{name}_grey.png')

        self.enabled = True # Can only press button when self.enabled = True
        self.pressed = False


    def clicked(self, mouse_pos:tuple[int]) -> bool:
        x,y = mouse_pos
        return (
            self.x_coor < x-4 < self.x_coor+BUTTON_HITBOX_SIZE and 
            self.y_coor < y-4 < self.y_coor+BUTTON_HITBOX_SIZE
        )
    
    
    def draw(self, screen):
        if self.enabled: png = self.pressed_png
        else: png = self.not_pressed_png
        screen.blit(png, (self.x_coor, self.y_coor))
