# heuristics.py - Contains the heuristic functions for the 8-puzzle solver

# Goal state for the puzzle
GOAL = ((0, 1, 2),
        (3, 4, 5),
        (6, 7, 8))

# hamming heuristic: returns the number of tiles in wrong position
# inputs: state (tuple of tuples representing the puzzle)
# outputs: number of misplaced tiles (int)
# function: counts how many tiles are not in their correct position
# time complexity: O(1) since it's always checking 9 positions
# space complexity: O(1) for storing the count
def hamming(state):
    count = 0
    # iterate through each tile
    for i in range(3):
        for j in range(3):
            # ignore blank tile
            if state[i][j] != 0:
                # the tile that *should* be at position [i][j] is at always at position [i*3+j]
                if state[i][j] != i * 3 + j:
                    # count goes up by 1 for each tile in wrong position
                    count += 1
    return count

# manhattan heuristic: returns the sum of distances each tile is from its goal
# inputs: state (tuple of tuples representing the puzzle)
# outputs: sum of manhattan distances (int)
# function: calculates total distance each tile needs to move to reach its goal position
# time complexity: O(1) since it's always checking 9 positions
# space complexity: O(1) for storing the distance sum
def manhattan(state):
    distance = 0
    # iterate through each tile
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            # ignore blank tile
            if tile != 0:
                # these two lines give the row/col where the tile actually belongs
                goal_row = tile // 3
                goal_col = tile % 3
                # abs gives absolute values (no negatives)
                # first term is vertical steps, second term is horizontal steps
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance
