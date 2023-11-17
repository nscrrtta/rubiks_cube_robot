#!/usr/bin/python3
from solve_scramble import solve, scramble
from button import Button
from cube import Cube
from face import Face
from box import Box
# import subprocess
import threading
import constants
# import motors
import pygame
import os


# Load window at the top edge of screen
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

pygame.init()
pygame.display.set_caption("Rubik's Cube Robot by Nick Sciarretta")
screen = pygame.display.set_mode((1024,571)) # Size of 7" touch screen


########### Objects/variables that create the GUI ###########
cube = Cube()

faces = [Face(i) for i in range(6)]
boxes = [Box (i) for i in range(6)]

FRU_png = pygame.image.load('png/FRU.png')
LBD_png = pygame.image.load('png/LBD.png')
red_x   = pygame.image.load('png/red_x.png')

solve_btn    = Button(482, 170, 'solve')
scramble_btn = Button(482, 257, 'scramble')
cancel_btn   = Button(482, 344, 'cancel')

selected_colour = selected_square = -1
running = solveable = True; cancel = False
#############################################################


# Main while loop -> draws GUI, gets user input, turns motors
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x,y = event.pos

            # Cancel
            if cancel_btn.clicked((x,y)): cancel = True
            elif cube.active or cube.moves: continue

            # Solve
            elif solve_btn.clicked((x,y)) and solveable:
                selected_colour = -1
                for box in boxes: box.selected = False
                # motors.GPIO.output(motors.enable_pin, 0)
                threading.Thread(target=solve, args=(cube,), daemon=True).start()

            # Scramble
            elif scramble_btn.clicked((x,y)) and solveable:
                selected_colour = -1
                for box in boxes: box.selected = False
                # motors.GPIO.output(motors.enable_pin, 0)
                threading.Thread(target=scramble, args=(cube,), daemon=True).start()

            # Select a sticker
            selected_square = -1
            for i, face in enumerate(faces):
                selected_square = face.get_clicked_square((x,y))
                if selected_square >= 0: break

            # Select a colour
            for box in boxes:
                if box.clicked((x,y)):
                    selected_colour = box.index
                    break

            # Change colour of sticker
            if selected_colour >= 0:
                for box in boxes:
                    box.selected = selected_colour == box.index

                if selected_square >= 0:

                    selected_square += 9*i
                    cube.sqrs[selected_square] = selected_colour
                    cube.set_centers([cube.sqrs[9*i+4] for i in range(6)])

                    solveable = cube.solveable()


    # Turn motors
    if cube.moves and not cancel:

        curr_move = cube.moves.pop(0)
        move_set = [curr_move]

        if cube.moves and cube.moves[0][0] == constants.opposite_faces[curr_move[0]]:
            move_set.append(cube.moves.pop(0)) # Next move can be made at the same time

        # threads:list[threading.Thread] = []
        # for move in move_set:
        #     m, n = move[0], int(move[1])
        #     motor = motors.motor_dict[m]
        #     threads.append(threading.Thread(target=motor.turn, args=(n,), daemon=True))

        # for thread in threads: thread.start()
        # for thread in threads: thread.join()

        for move in move_set: # Make move(s) in code to update GUI
            cube.make_move(move, save_move=False)

    elif not cube.active:

        if cancel: cancel = False
        if cube.moves: cube.moves = []

        for btn in [solve_btn, scramble_btn, cancel_btn]:
            if btn.pressed: btn.pressed = False

        # if not motors.GPIO.input(motors.enable_pin):
        #     motors.GPIO.output(motors.enable_pin, 1)


    # Draw GUI
    screen.fill((50,50,50))

    for i, face in enumerate(faces):
        face.draw(cube.sqrs[9*i:9*(i+1)], screen)

    for box in boxes:
        box.draw(screen)

    screen.blit(FRU_png, (20, 15))
    screen.blit(LBD_png, (923,15))
    
    for btn in [solve_btn, scramble_btn, cancel_btn]:
        btn.draw(screen)

    if not solveable: screen.blit(red_x, (480,167))

    pygame.display.update()


# motors.GPIO.cleanup()
pygame.quit()


# Shutdown Raspberry Pi
# subprocess.Popen('sudo shutdown -h now', stdout=subprocess.PIPE, shell=True)
