import numpy as np
import random

board_shape = [11, 11]
food_number = 15
path_length = 30
number_of_individuals = 10
initial_position = [int((board_shape[0] - 1) / 2), 
                    int((board_shape[1] - 1) / 2)]
mutation_rate = 0.1

def initialize_board(board_shape, num_of_food):
    board = np.zeros(shape = board_shape, dtype = np.int16)
    i = 0
    while i < num_of_food:
        x = random.randint(0,board_shape[0] - 1)
        y = random.randint(0,board_shape[1] - 1)
        if board[x, y] == 0:
            board[x, y] = 1
            i += 1
    return board

def initialize_path(path_length):
    path = []
    for _ in range(path_length):
        path.append(random.randint(0, 3))
    return np.array(path)

def is_it_alive(pos, shape):
    if pos[0] < 0 or pos[1] < 0 or pos[0] == shape[0] or pos[1] == shape[1]:
        return False
    else:
        return True

def walk_through(path, init_pos, board_shape):
    steps = np.array(init_pos)
    current_pos = init_pos
    for i in path:
        if i == 0: #go up
            current_pos[0] -= 1
        elif i == 1: #go right
            current_pos[1] += 1
        elif i == 2: #go down
            current_pos[0] += 1
        elif i == 3: #go left
            current_pos[1] -= 1
        if is_it_alive(current_pos, board_shape):
            steps = np.append(steps, current_pos)
        else:
            break
    return np.reshape(steps, [int(len(steps) / 2), 2])

def fitness_function(board, steps):
    fitness_val = 0
    for step in steps:
        if board[steep[0], step[1]] == 1:
            fitness_val += 1
    return fitness_val

def generate_first_generation(number_of_individuals, path_length):
    individuals = np.empty(shape = [number_of_individuals, path_length],
                           dtype = np.int16)
    for i in range(number_of_individuals):
        individuals[i] = initialize_path(path_length)
    return individuals

def cross_over(first_parent, second_parent):
    cross_over_line = random.randint(0, len(first_parent) - 1)
    first_child = np.append(first_parent[:cross_over_line],
                            second_parent[cross_over_line:])
    second_child = np.append(second_parent[:cross_over_line],
                             first_parent[cross_over_line:])
    return first_child, second_child

def give_mutation(individual, percentage_of_mutation):
    if random.uniform(0, 1) >= percentage_of_mutation: 
        mutated_gen = random.randint(0, len(individual) - 1)
        individual[mutated_gen] = random.randint(0, 3)
    return individual

def rank_individuals(board, individuals, initial_pos):
    fitnesses = []
    for ind in individuals:
        steps = walk_through(ind, initial_pos)
        fitnesses.append(fitness_function(board, steps))
    fitnesses = np.array(fitnesses)
    ranked_indices = fitnesses.argsort(fitnesses)
    return ranked_indices

def find_where_random_number_falls(length):
    total_score = (length * (length + 1)) / 2
    rand_int = random.randint(0, total_score - 1)
    intervals = [0]
    for i in range(2 ,length + 1):
        intervals.append(intervals[-1] + i)
    for i in range(intervals):
        if rand_int < intervals[i]:
            break
    return length - i - 1

def find_lucky_parents(ranked_indices):
    length = len(ranked_indices)
    first_parent = ranked_indices[find_where_random_number_falls(length)]
    second_parent = ranked_indices[find_where_random_number_falls(length)]
    while second_parent == first_parent:
        second_parent = ranked_indices[find_where_random_number_falls(length)]
    return first_parent, second_parent

def generate_new_generation(old_generation, mutation_rate):
    ranked_indices = rank_individuals(old_generation)
    new_generation = []
    for i in range(2, 0, len(old_generation)):
        first_parent_index, second_parent_index = find_lucky_parents(ranked_indices)
        first_parent  = old_generation[first_parent_index]
        second_parent = old_generation[second_parent_index]
        first_child, second_child = cross_over(first_parent, second_parent)
        first_child = give_mutation(first_child, mutation_rate)
        second_child = give_mutation(second_child, mutation_rate)
        new_generation.append(first_child)
        new_generation.append(second_child)
    return np.array(new_generation)

def print_path_on_board(board, steps):
    map = np.chararray(board.shape, unicode = True)
    map[:] = "1 "
    for step in steps:
        if board[step[0], step[1]] == 0:
            map[step[0], step[1]] = '='
        else:
            map[step[0], step[1]] = '+'
    map[steps[0,0], steps[0,1]] = "s"
    map[steps[-1,0], steps[-1,1]] = "f"
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            print(map[i, j], end = " ")
        print("\n", end = "")




board = initialize_board(board_shape, food_number)
generation = generate_first_generation(number_of_individuals, path_length)