# puzzle_utils.py - Utility functions for the 8-puzzle solver

import random
from heuristics import GOAL

# finds the position of the blank tile in the puzzle
# inputs: state (tuple of tuples representing the puzzle)
# outputs: row and column coordinates of the blank tile (tuple of ints)
# function: searches through the puzzle to locate the empty space (represented by 0)
# time complexity: O(1) since it's always checking 9 positions
# space complexity: O(1) for storing the coordinates
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# checks if a puzzle state can be solved
# inputs: state (tuple of tuples representing the puzzle)
# outputs: True if solvable, False otherwise (boolean)
# function: counts inversions to determine if the puzzle has a solution
# time complexity: O(n^2) where n is the number of tiles (9), so O(1) in practice
# space complexity: O(n) for the flattened list, so O(1) in practice
def is_solvable(state):
    # "flatten" the puzzle into a list of tiles (this makes the blank disappear)
    # we want it to disappear because it doesn't count as a tile, so it doesn't count towards inversions)
    flat = []
    for row in state:
        for num in row:
            if num != 0:
                flat.append(num)

    # initialize inversions to 0
    # count inversions (how many times a tile is larger than its neighbor)
    # if the neighbor is larger, then the tile is an inversion
    # if the neighbor is smaller, then the tile is not an inversion
    # the puzzle is solvable if the number of inversions is even
    inversions = 0
    for i in range(len(flat)): # len returns the number of elements in the (flattened) list
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1

    # returns True if puzzle is solvable (even number of inversions), False otherwise
    return inversions % 2 == 0

# generates all possible next states from the current state
# inputs: state (tuple of tuples representing the puzzle)
# outputs: list of (next_state, move) tuples
# function: finds all valid moves from the current state and returns the resulting states
# time complexity: O(1) since there are at most 4 possible moves
# space complexity: O(1) since we return at most 4 neighbors
def get_neighbors(state):
    # initialize list
    neighbors = []
    # find coordinates of the blank tile
    i, j = find_blank(state)
    # define the four possible moves
    moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]

    # try each direction; compute target coordinates (ni, nj) where the blank would land
    for di, dj, move in moves:
        ni, nj = i + di, j + dj
        # the if clause is a boundary check - we must stay inside the 3x3 grid
        if 0 <= ni < 3 and 0 <= nj < 3:
            # turn state (tuple of tuples) into a list of lists so we can swap elements
            new_state = [list(row) for row in state]
            # value at the blank [i][j] and value at [ni][nj] is swapped
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            # after the swap, convert list of lists back into tuple of tuples
            new_state = tuple(tuple(row) for row in new_state)
            # records result as a pair
            # new_state =  board after the move
            # move = name of move (UP, DOWN etc)
            neighbors.append((new_state, move))

    # return list of up to 4 neighbors
    return neighbors

# generates a random solvable puzzle state
# inputs: none
# outputs: random solvable state (tuple of tuples)
# function: keeps generating random states until it finds one that can be solved
# time complexity: O(1) on average, but could be O(n) in worst case
# space complexity: O(1) for storing the state
def generate_random_solvable_board():
    # keep trying until we get a solvable puzzle
    while True:
        # create a list of numbers 0-8 and shuffle them randomly
        tiles = list(range(9))
        random.shuffle(tiles)
        # convert the flat list into a 3x3 grid (tuple of tuples)
        state = tuple(tuple(tiles[i*3:i*3+3]) for i in range(3))
        # only return if this state is actually solvable
        if is_solvable(state):
            return state
