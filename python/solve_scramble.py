from random import choice
from constants import *
from cube import Cube
import itertools


def solve(root_cube: Cube):
    """
    This function solves the cube using the CFOP method 
    (cross, first two layers, orientation of last layer, permutation of last layer)

    It explores multiple ways to solve the cube, 
    and chooses the shortest list of moves it could find
    """
    root_cube.active = True
    cube = Cube(root_cube.sqrs[:])    
    centers = (back, left, up, right, down, front) = [cube.sqrs[9*i+4] for i in range(6)]


    # Cross
    cross_cubes = {}
    for permutation in itertools.permutations([front,right,back,left]):
        cube.cross(list(permutation), cross_cubes)


    # Sort in order of numer of moves (low -> high)
    cross_cubes = dict( sorted( cross_cubes.items(), key=lambda x: len(x[0]) )[:10] )


    # F2L
    f2l_cubes = {}
    for moves, sqrs in cross_cubes.items():
   
        sub_cube = Cube(list(sqrs))
        sub_cube.set_centers(centers)
        sub_cube.moves = list(moves)

        for permutation in itertools.permutations([(front,left),(right,front),(back,right),(left,back)]):
            sub_cube.F2L(list(permutation), f2l_cubes)
            # Comment out break statement below to explore all permutations
            # (warning: code will slow down)
            break


    # Sort in order of numer of moves (low -> high)
    f2l_cubes = dict( sorted( f2l_cubes.items(), key=lambda x: len(x[0]) )[:10] )


    # OLL and PLL
    solved_cubes = {}
    for moves, sqrs in f2l_cubes.items():
        
        sub_cube = Cube(list(sqrs))
        sub_cube.set_centers(centers)
        sub_cube.moves = list(moves)

        sub_cube.OLL()
        sub_cube.PLL()

        sub_cube.organize_moves(sub_cube.moves, no_U=True)
        solved_cubes[tuple(sub_cube.moves)] = tuple(sub_cube.sqrs)


    # Sort in order of numer of moves (low -> high)
    solved_cubes = sorted( list(solved_cubes), key=lambda x: len(x) )
    shortest_solution = list(solved_cubes[0])

    root_cube.moves = shortest_solution
    root_cube.active = False


def scramble(root_cube: Cube):

    root_cube.active = True
    scramble = []
    
    while len(scramble) < 20:
        scramble.append(choice([F, B, L, R, D]))
        root_cube.organize_moves(scramble)

    root_cube.moves = scramble
    root_cube.active = False
