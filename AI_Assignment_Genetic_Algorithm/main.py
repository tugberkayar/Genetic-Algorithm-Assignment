from World import World
from Individual import Individual
from Generation import Generation
from os import system
from colorama import init, Fore, Back
from msvcrt import getch
import numpy as np

init(convert = True)
world_color_map = [Back.WHITE, Back.RED]
travel_color_map = [Back.WHITE, Back.RED,Back.BLACK,  Back.GREEN]

def print_array_colored(array, color_map):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            print(color_map[array[x, y]] + " ", end = "")
        print("\n", end = "")
    print(Back.BLACK)


def build_travel_array(positions, world):
    travel_map = np.array(world.map)
    for pos in positions:
        if world.map[pos[0], pos[1]] == 0:
            travel_map[pos[0], pos[1]] = 2
        else:
            travel_map[pos[0], pos[1]] = 3
    return travel_map

def print_travel_maps(best, middle, worst, color_map):
    print("BEST", end = "")
    print(" " * World.SHAPE[1], end = "")
    print("MIDDLE", end = "")
    print(" " * (World.SHAPE[1] - 2), end = "")
    print("WORST")
    for x in range(best.shape[0]):
        for y in range(best.shape[1]):
            print(color_map[best[x, y]] + " ", end = "")
        print(Back.BLACK + "    ", end = "")
        for y in range(best.shape[1]):
            print(color_map[middle[x, y]] + " ", end = "")
        print(Back.BLACK + "    ", end = "")
        for y in range(best.shape[1]):
            print(color_map[worst[x, y]] + " ", end = "")
        print(Back.BLACK + "    ")
    

    


def print_generation_information(world, gnr, gnr_count, paint_mode):
    system('cls')
    print("\nGENERATION " + str(gnr_count))
    print("\n\nWorld Size           :" + str(world.SHAPE))
    print("Number of Food       : " + str(world.NUM_OF_FOOD))
    print("Number Of Individuals:" + str(gnr.NUM_OF_INDIVIDUALS))
    print("\nMost Eaten Food      :" + str(gnr.individuals[0].eaten_food))
    print("Best Fitness         :" + str(gnr.individuals[0].fitness))
    print("Average Eaten Fodd   :" + str(gnr.average))
    print("Average Fitness      :" + str(gnr.average_fitness))
    if gnr_count % paint_mode == 0:
        print("\n\nBOARD\n")
        print_array_colored(world.map, world_color_map)

        middle_index = int(len(gnr.individuals) / 2)

        print_travel_maps(build_travel_array(gnr.individuals[0].positions, world),
                          build_travel_array(gnr.individuals[middle_index].positions, world),
                          build_travel_array(gnr.individuals[-1].positions, world), travel_color_map)
        getch()
    
    



world = World()
gnr = Generation(world)
gnr_count = 0
print_generation_information(world, gnr, gnr_count, 50)

while gnr.individuals[0].eaten_food < World.NUM_OF_FOOD and  gnr_count < 2000:
    gnr = Generation(world = world, ancestor_individuals = gnr)
    gnr_count += 1
    print_generation_information(world, gnr,  gnr_count, 50)
    
print_generation_information(world, gnr,  gnr_count, gnr_count)

