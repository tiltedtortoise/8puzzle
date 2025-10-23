# solver.py - A* search algorithm for solving the 8-puzzle

import time
import heapq
from heuristics import GOAL, hamming, manhattan
from puzzle_utils import get_neighbors, is_solvable

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

# calculates the costs (g, h, f) for a given state
# inputs: state (tuple of tuples), parent node, move, heuristic function
# outputs: g cost, h cost, f cost (all integers)
# function: computes the path cost and heuristic estimate for a state
# time complexity: O(1) for cost calculation
# space complexity: O(1) for storing costs
def calculate_costs(state, parent, move, heuristic_func):
    g = parent.g + 1 if parent else 0  # path cost from start
    h = heuristic_func(state)  # heuristic estimate to goal
    f = g + h  # total estimated cost
    return g, h, f

# main solving function using a* search algorithm
# inputs: start state (tuple of tuples), heuristic name (string)
# outputs: solution path (list of moves), nodes expanded (int), time taken (float)
# function: finds the shortest path from start to goal using the specified heuristic
# time complexity: O(b^d) where b is branching factor (max 4) and d is solution depth
# space complexity: O(b^d) for storing all nodes in memory
def solve(start, heuristic='manhattan'):
    # first check if the puzzle can actually be solved
    if not is_solvable(start):
        return None

    # if we're already at the goal, no moves needed
    if start == GOAL:
        return [], 0, 0.0

    # pick which heuristic function to use based on the parameter
    if heuristic == 'manhattan':
        h_func = manhattan
    else:
        h_func = hamming

    # start timing how long the search takes
    start_time = time.time()
    nodes_expanded = 0

    # create the starting node with initial costs
    start_node = Node(start, None, None, 0, h_func(start))
    # frontier is our priority queue of nodes to explore (open list)
    frontier = [start_node]
    # explored is our set of nodes we've already looked at (closed list)
    explored = set()
    # best_cost keeps track of the cheapest way we've found to reach each state
    best_cost = {start: 0}

    # keep searching until we run out of nodes to explore
    while frontier:
        # get the node with the lowest f cost from the priority queue
        current = heapq.heappop(frontier)

        # skip if we've already fully explored this state
        if current.state in explored:
            continue

        # mark this state as explored so we don't look at it again
        explored.add(current.state)
        nodes_expanded += 1

        # check if we found the goal
        if current.state == GOAL:
            # reconstruct the path by following parent pointers backwards
            path = []
            node = current
            while node.parent:
                path.append(node.move)
                node = node.parent
            # reverse the path since we built it backwards
            path.reverse()
            return path, nodes_expanded, time.time() - start_time

        # look at all possible moves from the current state
        for next_state, move in get_neighbors(current.state):
            # skip if we've already explored this state
            if next_state in explored:
                continue

            # calculate the cost to reach this new state (one more move)
            new_g = current.g + 1

            # skip if we've already found a cheaper way to reach this state
            if next_state in best_cost and best_cost[next_state] <= new_g:
                continue

            # update the best cost to reach this state
            best_cost[next_state] = new_g
            # calculate heuristic estimate for remaining distance
            h = h_func(next_state)
            # create new node and add it to the frontier
            next_node = Node(next_state, current, move, new_g, h)
            heapq.heappush(frontier, next_node)

    # if we get here, no solution was found (shouldn't happen for solvable puzzles)
    return None
