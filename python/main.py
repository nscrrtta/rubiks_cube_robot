#!/usr/bin/python3
from motors import Motors
from constants import *
from gui import GUI
import pygame


pygame.init()

motors = Motors()
gui = GUI()
moves = []

# Main while loop -> gets user input, turns motors, draws GUI
while True:

    events = [event.type for event in pygame.event.get()]

    if pygame.QUIT in events: break
    elif pygame.MOUSEBUTTONDOWN in events:
        mouse_pos = pygame.mouse.get_pos()
        gui.handle_mouse_click(mouse_pos, motors.busy)

    gui.draw()

    if gui.abort_btn.pressed:
        gui.abort_btn.pressed = False
        moves = []

    elif gui.solve_btn.pressed:
        gui.solve_btn.pressed = False
        t = time.time()
        moves = gui.cube.solve()
        print(f'{len(moves)} moves in {round(time.time()-t, 2)} seconds')
        for i in range(0, len(moves), 10): print(moves[i : i+10])
        print()
        motors.set_enable_pin(0)

    elif gui.scrmb_btn.pressed:
        gui.scrmb_btn.pressed = False
        moves = gui.cube.scramble()
        motors.set_enable_pin(0)
        print(f'scramble: {moves}')

    if moves:
        move1 = moves.pop(0)
        
        # If able to do two moves at once
        if moves and moves[0][0] == OPPOSITE_FACES[move1[0]]: move2 = moves.pop(0)
        else: move2 = None

        motors.turn(move1, move2)
        
        # Update GUI
        gui.cube.turn_face(gui.cube.sqrs, move1)
        if move2 is not None: gui.cube.turn_face(gui.cube.sqrs, move2)

    # After completing last move
    if motors.busy and moves == []:
        motors.set_enable_pin(1)
        gui.reset_buttons()

# motors.cleaup_pins()
pygame.quit()