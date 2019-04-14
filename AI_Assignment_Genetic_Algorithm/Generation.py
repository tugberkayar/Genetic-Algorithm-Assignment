import numpy as np
import random
from World import World
from Individual import Individual

class Generation:
    """
    A class that holds all the information about individuals in a generation.
    Responsible for creating new generations.

    Attributes
        NUM_OF_INDIVIDUALS:     Number of individuals in a generation. Integer value. Class attribute.
        MUTATION_RATE:          Mutation rate. Float value between 0 and 1. Class attribute.
        PERCENTAGE_INTERVALS:   Defines probability intervals for each individual. 
                                Assigns 1 to least successfull individual, 2 to second last and so on.
        individuals:            Numpy array of Individual class. It's length is NUM_OF_INDIVIDUALS.
                                Holds current generation.
    """
  
    NUM_OF_INDIVIDUALS = 1000
    MUTATION_RATE = 0.08
    

    def __init__(self, world, ancestor_individuals = []):
        Generation.PERCENTAGE_INTERVALS = Generation.calculate_percentage_interval()
        if ancestor_individuals == []:
            self.individuals = Generation.generate_first_generation(world)
        else:
            self.individuals = Generation.init_from_old_generation(ancestor_individuals, world)
            self.give_mutation_to_new_generation()
        self.average = self.average_eaten_food()
        self.average_fitness = self.calculate_average_fitness()

    @staticmethod
    def generate_first_generation(world):
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
            for step in ind.steps:
                if random.uniform(0, 1) > self.MUTATION_RATE:
                    new_gene = random.randint(0, 3)
                    ind.steps[step] = new_gene


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

    def average_eaten_food(self):
        sum = 0
        for ind in self.individuals:
            sum += ind.eaten_food
        return sum / self.NUM_OF_INDIVIDUALS

    def calculate_average_fitness(self):
        sum = 0
        for ind in self.individuals:
            sum += ind.fitness
        return sum / len(self.individuals)

