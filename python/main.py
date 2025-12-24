#!/usr/bin/python3
from Motors.motors import Motors
from Cube.solver import Solver
from Cube.cube import Cube
from GUI.gui import GUI
import pygame


pygame.init()

cube = Cube()
gui = GUI(cube)
solver = Solver(cube)
motors = Motors()
moves: list[tuple[int]] = []

gui.draw()
running = True

# Main while loop -> gets user input, turns motors, draws GUI
# GUI is mostly static so it doesn't need to be updated every frame
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if gui.handle_mouse_click(mouse_pos, motors.busy):
                gui.draw()

    if gui.abort_btn.pressed:
        gui.abort_btn.pressed = False
        moves = []

    elif gui.solve_btn.pressed:
        gui.solve_btn.pressed = False
        moves = solver.solve()
        motors.set_enable_pin(0)

    elif gui.scrmb_btn.pressed:
        gui.scrmb_btn.pressed = False
        moves = solver.scramble()
        motors.set_enable_pin(0)

    elif moves:
        move1, move2 = moves.pop()
        motors.turn(move1, move2)
        
        cube.make_move(move1, save=False)
        if move2: cube.make_move(move2, save=False)
        if gui.show_num_moves: gui.increment_num_moves()

        gui.draw()
        
    # After completing last move
    elif motors.busy:
        motors.set_enable_pin(1)
        gui.reset_buttons()
        gui.draw()

motors.cleanup_pins()
pygame.quit()
