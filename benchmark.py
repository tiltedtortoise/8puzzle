# benchmark.py - Performance testing for the 8-puzzle solver

import statistics
from puzzle_utils import generate_random_solvable_board, GOAL
from solver import solve

# runs performance tests on both heuristics with random puzzles
# inputs: n (number of puzzles to test, default 100)
# outputs: none (prints results to console)
# function: tests both heuristics on random puzzles and shows statistics
# time complexity: O(n * b^d) where n is number of tests, b is branching factor, d is depth
# space complexity: O(n) for storing results
def run_benchmark(n=100):
    # print header for the test run
    print("\n" + "="*60)
    print("8-Puzzle Solver - Testing", n, "random puzzles")
    print("="*60)

    # lists to store performance data for each heuristic
    hamming_times = []
    hamming_nodes = []
    manhattan_times = []
    manhattan_nodes = []

    # test each random puzzle with both heuristics
    for i in range(n):
        # show progress (overwrites the same line)
        print(f"Test {i+1}/{n}", end='\r')

        # generate a random solvable puzzle
        state = generate_random_solvable_board()
        # skip if we accidentally got the goal state (no moves needed)
        if state == GOAL:
            continue

        # test with hamming heuristic
        result = solve(state, 'hamming')
        if result:
            _, nodes, t = result
            hamming_nodes.append(nodes)
            hamming_times.append(t)

        # test with manhattan heuristic
        result = solve(state, 'manhattan')
        if result:
            _, nodes, t = result
            manhattan_nodes.append(nodes)
            manhattan_times.append(t)

    # print the results in a nice table format
    print("\n\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Puzzles solved: {len(hamming_times)}/{n}\n")

    # print table headers
    print(f"{'Metric':<25} {'Hamming':<15} {'Manhattan':<15}")
    print("-"*60)
    # print average execution times
    print(f"{'Avg Time (s)':<25} {sum(hamming_times)/len(hamming_times):<15.4f} {sum(manhattan_times)/len(manhattan_times):<15.4f}")
    # print standard deviation of execution times
    print(f"{'Std Dev Time':<25} {statistics.stdev(hamming_times):<15.4f} {statistics.stdev(manhattan_times):<15.4f}")
    # print average number of nodes expanded
    print(f"{'Avg Nodes':<25} {sum(hamming_nodes)/len(hamming_nodes):<15.1f} {sum(manhattan_nodes)/len(manhattan_nodes):<15.1f}")
    # print standard deviation of nodes expanded
    print(f"{'Std Dev Nodes':<25} {statistics.stdev(hamming_nodes):<15.1f} {statistics.stdev(manhattan_nodes):<15.1f}")
    # print minimum and maximum nodes for comparison
    print(f"{'Min Nodes':<25} {min(hamming_nodes):<15} {min(manhattan_nodes):<15}")
    print(f"{'Max Nodes':<25} {max(hamming_nodes):<15} {max(manhattan_nodes):<15}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_benchmark(100)
