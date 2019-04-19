"""
Title: CS461 HW2
Authors: Khasmamad Shabanovi   21701333
         Mohamad Fakhouri      21701546
         Ayman Rehan           21500101
         Muhammad Junaid Iqbal 21503709
Heuristics: Program uses heuristic no. 1
"""


import random
import copy

def main():
    puzzle_container = puzzle_generator()
    if puzzle_container == None:
        pass

    w = 2
    path_container = {2: [], 3: []}
    for i in range(2):
        print("Starting Beam Search with w = {0}...".format(w))
        for i in range(len(puzzle_container)):
            print("Solving puzzle no. {0}".format(i + 1))

            check_dict = {}
            puzz = []
            puzz.append(puzzle_container[i])
            path, goal = beam_search(puzz, check_dict, w)
            path_container[w].append((path, len(path) - 1, goal))
            print("")
        print("")
        w += 1

    shortest_path, index_of_shortest = find_shortest_path(path_container)
    print_path(shortest_path, index_of_shortest)

def printCSV(path_container):
    print("Puzzle Number, Move count (with w = 2), Move count (with w = 3)")
    for i in range(25):
        #printing puzzle number, moves in w = 2, moves in w = 3

        if path_container[2][i][2] == False:
            firstCount = "NoSol"
        else:
            firstCount = path_container[2][i][1]

        if path_container[3][i][2] == False:
            secondCount = "NoSol"
        else:
            secondCount = path_container[3][i][1]
        stringToPrint = "" + str(i + 1) +"," + str(firstCount) + "," + str(secondCount)
        print(stringToPrint)


def getMove(oldIndex, newIndex):
    dx = newIndex[0] - oldIndex[0]
    dy = newIndex[1] - oldIndex[1]

    if dx > 0:
        return "left"
    elif dx < 0:
        return "right"
    elif dy > 0:
        return "up"
    elif dy < 0:
        return "down"
    else:
        return ""


def getValue(oldState, newIndex):
    return oldState[newIndex[1]][newIndex[0]]


def print_path(path, index):

    print("Printing trace for puzzle no. {0} (solved with w = {1}):".format(index[1], index[0]))
    print_puzzle(path[0][0])
    for i in range(1, len(path)):
        movement = getMove(path[i-1][1], path[i][1])

        movedTile = getValue(path[i-1][0], path[i][1])
        print(i, ": move ", movedTile, " ", movement, sep="")
        print_puzzle(path[i][0])
        print('')


def find_shortest_path(path_container):
    index_of_shortest = ()
    min_ = 99999
    for i in range(len(path_container[2])):
        if path_container[2][i][2]:
            if path_container[2][i][1] < min_ and path_container[2][i][1] > 0:
                shortest_path = path_container[2][i][0]
                min_ = path_container[2][i][1]
                index_of_shortest = (2, i)

    for i in range(len(path_container[3])):
        if path_container[3][i][2]:
            if path_container[3][i][1] < min_ and path_container[3][i][1] > 0:
                shortest_path = path_container[3][i][0]
                min_ = path_container[3][i][1]
                index_of_shortest = (3, i + 1)

    return shortest_path, index_of_shortest

def been_there(state, check_dict, check):
    key = str(state)
    if key in check_dict:
        return True
    else:
        if check:
            check_dict[key] = True
        return False


def puzzle_generator():
    print("Generating puzzles...")
    initial_state_tuple = ([[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]], (0, 0))
    puzzle_container = []
    while len(puzzle_container) < 25:
        next_state_tuple = ()
        check_dict = {}
        for i in range(15):
            state_container = next_possible_states(initial_state_tuple, check_dict, True)
            try:
                next_state_tuple = random.choice(state_container)
                initial_state_tuple = next_state_tuple
            except IndexError:
                if initial_state_tuple not in puzzle_container:
                    puzzle_container.append(initial_state_tuple)
                break
        if i == len(puzzle_container):
            if next_state_tuple not in puzzle_container:
                puzzle_container.append(next_state_tuple)
    if len(puzzle_container) == 25:
        print("25 distinct puzzles are succesfully generated!")
        return puzzle_container
    else:
        print("Puzzle generation failed!")


def next_possible_states(current_state_tuple, check_dict, check):
    state_container = []
    x = current_state_tuple[1][0]
    y = current_state_tuple[1][1]
    current_state = current_state_tuple[0]

    # Down
    if y < 3:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y + 1][x]
        new_state[y + 1][x] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x, y + 1)
            h1 = calculate_h1(new_state)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    # Up
    if y > 0:
        new_state = copy.deepcopy(current_state)
        if y == 1 and x == 0:
            new_state[y][x] = new_state[y - 1][x]
            new_state[y - 1][x] = 0
            if is_goal(new_state):
                new_index = (x, y - 1)
                h1 = calculate_h1(new_state)
                new_state_tuple = (new_state, new_index, h1)
                state_container.append(new_state_tuple)
        elif y > 1:
            new_state[y][x] = new_state[y - 1][x]
            new_state[y - 1][x] = 0
            if not been_there(new_state, check_dict, check):
                new_index = (x, y - 1)
                h1 = calculate_h1(new_state)
                new_state_tuple = (new_state, new_index, h1)
                state_container.append(new_state_tuple)

    # Left
    if x > 0 and y > 0:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y][x - 1]
        new_state[y][x - 1] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x - 1, y)
            h1 = calculate_h1(new_state)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    # Right
    if x < 2 and y > 0:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y][x + 1]
        new_state[y][x + 1] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x + 1, y)
            h1 = calculate_h1(new_state)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    return state_container


def print_puzzle(state):
    print('-----')
    for i in range(4):
        print('|', end="")
        for j in range(3):
            if state[i][j] == 0:
                print("   |", end="")
            else:
                print("", state[i][j], "|", end="")
            if i == 0:
                break
        print('\n-------------')


def is_goal(state):
    goal_state = [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return state == goal_state


def calculate_h1(state):
    h1 = 0
    goal_state = [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for y in range(len(goal_state)):
        for x in range(len(goal_state[y])):
            if state[y][x] != goal_state[y][x]:
                h1 += 1
    return h1


def beam_search(initial_state, check_dict, w):
    print("Implementing Beam Search...")

    q = []
    q.append(initial_state)
    accomplished = False

    while len(q) != 0:
        candidates = []
        for i in range(len(q)):
            path = q.pop()

            if is_goal(path[-1][0]):
                goal = path
                accomplished = True
                break

            state_container = next_possible_states(path[-1], check_dict, False)
            for i in state_container:
                temp = list(path)
                temp.append(i)
                candidates.append(temp)

        if accomplished:
            break

        candidates.sort(key=lambda x: x[-1][2])
        for i in range(min(len(candidates), w)):
            if not been_there(candidates[i][-1][0], check_dict, True):
                q.append(candidates[i])

    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        return path, False


if __name__ == "__main__":
    main()