import numpy as np
import random

class World:
    """A class that holds the information about the
    board and places of food.

    Attributes
        SHAPE:          Shape of the world. It has two values in it. First value
                        represents the row, second represents column number. dtype = python list.
                        Class attribute.
        NUM_OF_FOOD:    Integer value. Specifies how many foods will there 
                        be in the world. Class attribute. dttype: int
        map:            Map of the world. Foods are represented by 1, empty fields are
                        represented by 0. type: np.ndarray
    """
    
    SHAPE = [15, 15]
    NUM_OF_FOOD = 15

    def __init__(self):
        self.map = World.initialize_map()

    @staticmethod
    def initialize_map():
        """initializes the map of the world. Returns np.ndarray that it's
        shape is equal to World.SHAPE.
        """
        map = np.zeros(shape = World.SHAPE, dtype = np.int16)
        i = 0
        while i < World.NUM_OF_FOOD:
            x = random.randint(0,World.SHAPE[0] - 1)
            y = random.randint(0,World.SHAPE[1] - 1)
            if map[x, y] == 0:
                map[x, y] = 1
                i += 1
        return map
   

class Individual:
    """A class that holds informations about each individual in a generation.

    Attributes
        STEP_SIZE:      Max step size that an individual can go. dtype: int
        INIT_POSITION:  Initial position of individuals. They start in the middle of the world.
                        Class attribute. dtype: python list. First value represents row, second represeents column.
        steps:          Info about which direction will the instance go in every round.
                        0 refers uo, 1 refers right, 2 refers down and 3 refers left.
                        It's length is STEP_SIZE.
        positions:      It specifies where will be the individual after every step it has taken
                        until either it is dead, or it reaches the STEP_SIZE. dtype: np.ndarray
        eaten_food:     specifies how many food has eaten by the individual. Integer value.
        fittness:       specifies how successfull the individual is. Integer value.
    """
    
    STEP_SIZE = 450
    INIT_POSITION = [int((World.SHAPE[0] - 1) / 2),                      int((World.SHAPE[1] - 1) / 2)]

    def __init__(self, world, steps = []):
        if steps == []:
            self.steps = Individual.init_without_parents()
        else:
            self.steps = steps
        self.positions = self.walk_through()
        self.eaten_food = self.eaten_food_count(world.map)
        self.fitness = self.fitness_function()
    
    @staticmethod
    def init_without_parents():
        """randomly creates a numpy array. The values are between 0 and 3.
        Length equals STEP_SIZE.
        """
        steps = []
        for _ in range(Individual.STEP_SIZE):
            steps.append(random.randint(0, 3))
        return np.array(steps)
    
    @staticmethod
    def is_position_in_the_world(pos):
        """Checks if the updated position of an
        individual is still in the world, or it is dead.

        Args
            pos:    Coords of the updated position.
            Return: Returns if the position still in the world, returns True; False otherwise.
        """
        if pos[0] < 0: #went too up
            return False
        elif pos[1] < 0: # went too left
            return False
        elif pos[0] == World.SHAPE[0]: #went too down
            return False
        elif pos[1] == World.SHAPE[1]: #went too right
            return False
        else:
            return True

    def walk_through(self):
        """Walks through on the map with the given steps, until
        the all steps are processed, or the individual is dead.
        Returns the coordinates saved after every step.
        """
        positions = np.array(Individual.INIT_POSITION)
        current_pos = np.array(Individual.INIT_POSITION)
        for step in self.steps:
            if step == 0: #go up
                current_pos[0] -= 1
            elif step == 1: #go right
                current_pos[1] += 1
            elif step == 2: #go down
                current_pos[0] += 1
            elif step == 3: #go left
                current_pos[1] -= 1
            if Individual.is_position_in_the_world(current_pos):
                positions = np.append(positions, current_pos)
            else:
                break
        return np.reshape(positions, [int(len(positions) / 2), 2])

    def eaten_food_count(self, map):
        """Counts how many food has been eaten by the individual.
        """
        copy_map = np.array(map)
        eaten_food = 0
        for pos in self.positions:
            if copy_map[pos[0], pos[1]] == 1:
                eaten_food += 1
                copy_map[pos[0]] = 0
        return eaten_food

    def how_many_different_points(self):
        """Counts how many different point the individual
        has stepped while walkind.
        """
        different_point_count = 0
        stepped_points = np.zeros(shape = World.SHAPE, dtype = np.int16)
        for pos in self.positions:
            if stepped_points[pos[0], pos[1]] == 0:
                different_point_count += 1
                stepped_points[pos[0], pos[1]] = 1
        return different_point_count

    def fitness_function(self):
        """Calculates how successfull the individual is.
        """
        return self.eaten_food * 5 + self.how_many_different_points() * 2


class Generation:
    """A class that holds all the information about individuals in a generation.
    Responsible for creating new generations.

    Attributes
        NUM_OF_INDIVIDUALS: Number of individuals in a generation. Integer value. Class attribute.
        MUTATION_RATE:      Mutation rate. Float value between 0 and 1. Class attribute.
        individuals:        Numpy array of Individual class. It's length is NUM_OF_INDIVIDUALS.
                            Holds current generation.
    """
  
    NUM_OF_INDIVIDUALS = 1000
    MUTATION_RATE = 0.2
    

    def __init__(self, world, ancestor_individuals = []):
        Generation.PERCENTAGE_INTERVALS = Generation.calculate_percentage_interval()
        if ancestor_individuals == []:
            self.individuals = Generation.generate_first_generation()
        else:
            self.individuals = Generation.init_from_old_generation(ancestor_individuals, world)
            self.give_mutation_to_new_generation()

    @staticmethod
    def generate_first_generation():
        """ Randomly generates the first generation and sorts them
        with regards to their fitness values. Returns np.ndarray of 
        Individaul class.
        """
        generation = np.empty(shape = Generation.NUM_OF_INDIVIDUALS,
                              dtype = Individual)
        for i in range(Generation.NUM_OF_INDIVIDUALS):
            generation[i] = Individual(world)
        return sorted(generation,
                      key = lambda ind: ind.fitness, reverse = True)

    def give_mutation_to_new_generation(self):
        """Gives mutation to every individual after creating a new generation.

        """
        for ind in self.individuals:
            if random.uniform(0, 1) > self.MUTATION_RATE:
                mutated_gene = random.randint(0, Individual.STEP_SIZE - 1)
                new_gene = random.randint(0, 3)
                ind.steps[mutated_gene] = new_gene
    
    @staticmethod
    def calculate_percentage_interval():
        """Calculates the probability of being selected of every
        individual. First index refers the most successfull, last index
        refers to least successfull individual.
        """
        percentage_intervals = [Generation.NUM_OF_INDIVIDUALS]
        for i in range(Generation.NUM_OF_INDIVIDUALS - 1, 0, -1):
           percentage_intervals.append(percentage_intervals[-1] + i)
        return percentage_intervals

    def select_index_from_individuals(self):
        """Selects index of an individual with respect to their selection probabilites.
        """
        total_score = Generation.NUM_OF_INDIVIDUALS * (Generation.NUM_OF_INDIVIDUALS + 1) / 2
        rand_int = random.randint(1, total_score)
        for i in range(len(Generation.PERCENTAGE_INTERVALS)):
            if rand_int <= Generation.PERCENTAGE_INTERVALS[i]:
                return i
            else:
                rand_int = random.randint(1, total_score)     

    def select_two_parents(self):
        """Selects two different parent for cross over.
        Returns the Individual class instances.
        """
        first_index = self.select_index_from_individuals()
        second_index = self.select_index_from_individuals()
        while first_index == second_index:
            second_index = self.select_index_from_individuals()
        return self.individuals[first_index], self.individuals[second_index] 

    @staticmethod
    def cross_over(first_parent, second_parent):
        """Applies one point cross over to given parents.
        Returns the steps of the results of the cross over.
        """
        
        cross_over_line = random.randint(0, Individual.STEP_SIZE - 1)
        first_child_steps = np.append(first_parent.steps[:cross_over_line],
                                second_parent.steps[cross_over_line:])
        second_child_steps = np.append(second_parent.steps[:cross_over_line],
                                 first_parent.steps[cross_over_line:])
        
        """
        first_child_steps, second_child_steps = [], []
        for i in range(Individual.STEP_SIZE):
            randon_binray_num = random.randint(0, 1)
            if randon_binray_num == 0:
                first_child_steps.append(first_parent.steps[i])
                second_child_steps.append(second_parent.steps[i])
            else:
                first_child_steps.append(second_parent.steps[i])
                second_child_steps.append(first_parent.steps[i])
        """
        return first_child_steps, second_child_steps
        
    @staticmethod 
    def init_from_old_generation(old_generation, world):
        """It generates new generation with given old one.
        Mutation needs to be given after this method.
        """
        new_generation = []
        for i in range(0, Generation.NUM_OF_INDIVIDUALS, 2):
            first_parent, second_parent = old_generation.select_two_parents()
            first_child_steps, second_child_steps = Generation.cross_over(first_parent, second_parent)
            new_generation.append(Individual(world, first_child_steps))
            new_generation.append(Individual(world, second_child_steps))
        return sorted(np.array(new_generation), 
                      key = lambda ind: ind.fitness, reverse = True)


world = World()
gnr = Generation(world)
gnr_count = 1
while gnr.individuals[0].eaten_food != World.NUM_OF_FOOD and gnr_count < 200:
    print("\nGeneration:", end = " ")
    print(gnr_count)
    print("Best Fitness:", end = " ")
    print(gnr.individuals[0].fitness, end = " ")
    print("Best Eaten Food:", end = " ")
    print(gnr.individuals[0].eaten_food)
    print("Differnet Positions:", end = " ")
    print(gnr.individuals[0].positions.shape[0])
    gnr = Generation(world = world, ancestor_individuals = gnr)
    gnr_count += 1


