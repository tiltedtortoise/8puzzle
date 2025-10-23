import random
import time
# heapq is important for comparing nodes in the priority queue
import heapq
# statistics is used for calculating standard deviations
import statistics

# Goal state for the puzzle
# this is a tuple of tuples, meaning the order of the tiles matters
GOAL = ((0, 1, 2),
        (3, 4, 5),
        (6, 7, 8))

# defines a node in the search tree
class Node:
    # constructor for a node in the search tree
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state # state of the board
        self.parent = parent # pointer to previous node so we can reconstruct path
        self.move = move # move that led to this state
        self.g = g  # cost from start (cost = how many moves it took to get to this node)
        self.h = h  # estimated cost to goal according to the heuristic (Hamming/Manhattan)
        self.f = g + h  # total cost that A* uses to decide which node to expand next

    # constructor for comparing nodes in the heap (the heap is the priority queue which A* uses)
    # lt = "less than"
    def __lt__(self, other):
        return self.f < other.f

# finds where the blank (0) tile is
# returns row, col of the blank tile
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# count inversions to check if puzzle can be solved
# inversions are when two tiles are in the wrong place
# puzzle is solvable if there is an even number of inversions
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

# Hamming heuristic: returns the number of tiles in wrong position
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

# Manhattan heuristic: returns the sum of distances each tile is from its goal
def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_row = tile // 3
                goal_col = tile % 3
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def get_neighbors(state):
    # generate possible moves
    neighbors = []
    i, j = find_blank(state)
    moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]

    for di, dj, move in moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            # swap blank with neighbor
            new_state = [list(row) for row in state]
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            new_state = tuple(tuple(row) for row in new_state)
            neighbors.append((new_state, move))

    return neighbors

def solve(start, heuristic='manhattan'):
    # A* search
    if not is_solvable(start):
        return None

    if start == GOAL:
        return [], 0, 0.0

    # pick which heuristic to use
    if heuristic == 'manhattan':
        h_func = manhattan
    else:
        h_func = hamming

    start_time = time.time()
    nodes_expanded = 0

    start_node = Node(start, None, None, 0, h_func(start))
    frontier = [start_node]
    explored = set()
    best_cost = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)

        if current.state in explored:
            continue

        explored.add(current.state)
        nodes_expanded += 1

        if current.state == GOAL:
            # reconstruct path
            path = []
            node = current
            while node.parent:
                path.append(node.move)
                node = node.parent
            path.reverse()
            return path, nodes_expanded, time.time() - start_time

        # expand neighbors
        for next_state, move in get_neighbors(current.state):
            if next_state in explored:
                continue

            new_g = current.g + 1

            if next_state in best_cost and best_cost[next_state] <= new_g:
                continue

            best_cost[next_state] = new_g
            h = h_func(next_state)
            next_node = Node(next_state, current, move, new_g, h)
            heapq.heappush(frontier, next_node)

    return None

def random_state():
    # make a random solvable puzzle
    while True:
        tiles = list(range(9))
        random.shuffle(tiles)
        state = tuple(tuple(tiles[i*3:i*3+3]) for i in range(3))
        if is_solvable(state):
            return state

def print_puzzle(state):
    print("-" * 13)
    for row in state:
        print("|", end="")
        for tile in row:
            if tile == 0:
                print("   |", end="")
            else:
                print(f" {tile} |", end="")
        print()
        print("-" * 13)

def run_tests(n=100):
    print("\n" + "="*60)
    print("8-Puzzle Solver - Testing", n, "random puzzles")
    print("="*60)

    hamming_times = []
    hamming_nodes = []
    manhattan_times = []
    manhattan_nodes = []

    for i in range(n):
        print(f"Test {i+1}/{n}", end='\r')

        state = random_state()
        if state == GOAL:
            continue

        # test hamming
        result = solve(state, 'hamming')
        if result:
            _, nodes, t = result
            hamming_nodes.append(nodes)
            hamming_times.append(t)

        # test manhattan
        result = solve(state, 'manhattan')
        if result:
            _, nodes, t = result
            manhattan_nodes.append(nodes)
            manhattan_times.append(t)

    print("\n\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Puzzles solved: {len(hamming_times)}/{n}\n")

    print(f"{'Metric':<25} {'Hamming':<15} {'Manhattan':<15}")
    print("-"*60)
    print(f"{'Avg Time (s)':<25} {sum(hamming_times)/len(hamming_times):<15.4f} {sum(manhattan_times)/len(manhattan_times):<15.4f}")
    print(f"{'Std Dev Time':<25} {statistics.stdev(hamming_times):<15.4f} {statistics.stdev(manhattan_times):<15.4f}")
    print(f"{'Avg Nodes':<25} {sum(hamming_nodes)/len(hamming_nodes):<15.1f} {sum(manhattan_nodes)/len(manhattan_nodes):<15.1f}")
    print(f"{'Std Dev Nodes':<25} {statistics.stdev(hamming_nodes):<15.1f} {statistics.stdev(manhattan_nodes):<15.1f}")
    print(f"{'Min Nodes':<25} {min(hamming_nodes):<15} {min(manhattan_nodes):<15}")
    print(f"{'Max Nodes':<25} {max(hamming_nodes):<15} {max(manhattan_nodes):<15}")
    print("="*60 + "\n")

def demo():
    print("\n" + "="*60)
    print("Demo - Solving one puzzle")
    print("="*60 + "\n")

    state = random_state()

    print("Start:")
    print_puzzle(state)
    print("\nGoal:")
    print_puzzle(GOAL)

    print("\nUsing Hamming heuristic...")
    path, nodes, t = solve(state, 'hamming')
    print(f"Solution: {len(path)} moves")
    print(f"Nodes expanded: {nodes}")
    print(f"Time: {t:.4f}s")

    print("\nUsing Manhattan heuristic...")
    path, nodes, t = solve(state, 'manhattan')
    print(f"Solution: {len(path)} moves")
    print(f"Nodes expanded: {nodes}")
    print(f"Time: {t:.4f}s")
    print()

if __name__ == "__main__":
    demo()
    run_tests(100)