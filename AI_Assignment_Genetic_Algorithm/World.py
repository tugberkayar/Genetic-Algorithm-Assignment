import numpy as np
import random

class World:
    """
    A class that holds the information about the
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
    
    SHAPE = [11, 11]
    NUM_OF_FOOD = 3

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
   
