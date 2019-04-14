import numpy as np
import random
from World import World

class Individual:
    """
    A class that holds informations about each individual in a generation.

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
    
    STEP_SIZE = 50
    INIT_POSITION = [int((World.SHAPE[0] - 1) / 2),                      
                     int((World.SHAPE[1] - 1) / 2)]

    def __init__(self, world, steps = []):
        if steps == []:
            self.steps = Individual.init_without_parents()
        else:
            self.steps = steps
        self.positions = self.walk_through()
        self.eaten_food = self.eaten_food_count(world.map)
        self.penalize_score = self.penalize_when_stepping_same_place()
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

    def penalize_when_stepping_same_place(self):
        step_count = np.zeros(World.SHAPE)
        penalize_score = 0
        for pos in self.positions:
            penalize_score += step_count[pos[0], pos[1]]
            step_count[pos[0], pos[1]] += 1
        return penalize_score

            
    
    def fitness_function(self):
        """Calculates how successfull the individual is.
        """
        fitness_val = self.eaten_food * 5
        fitness_val += self.how_many_different_points() * 3
        fitness_val -= self.penalize_score * 2
        return fitness_val

