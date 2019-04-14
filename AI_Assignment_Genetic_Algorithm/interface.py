from World import World
from Generation import Generation
from tkinter import *
import numpy as np

class GenerationPage(Frame):

    GENERATIONS = []
    ROOT = Tk()
    CURRENT_FRAME_INDEX = 0
    WORLD_COLOR_MAP = ['white', 'red']
    TRAVEL_COLOR_MAP = ['white', 'red', 'black', 'green']

    def __init__(self, world, generation, gnr_count, master = ROOT):
        Frame.__init__(self, master = master)
        self.world = world
        self.generation = generation
        self.gnr_count = gnr_count
        self.header_text = self.initialize_header()
        self.summary_text = self.initialize_sumary()
  
        self.top_frame =  Frame(self)
        self.top_left_frame =  Frame(self.top_frame)
        self.top_right_frame =  Frame(self.top_frame)
        self.middle_frame = Frame(self)
        self.bottom_frame = Frame(self)
        self.bottom_left_frame = Frame(self.bottom_frame)
        self.bottom_mid_frame = Frame(self.bottom_frame)
        self.bottom_right_frame = Frame(self.bottom_frame)
        
        self.header = Label(self.top_left_frame, text = self.header_text).grid(
                        row = 0, column = 0, columnspan = 2)

        self.prev_button = Button(self.top_left_frame, text = 'Prev Generation', 
                                  command = self.click_prev_button).grid(row = 1, column = 0)
        
        self.next_button = Button(self.top_left_frame, text = 'Next Generation', 
                                  command = self.click_next_button).grid(row = 1, column = 1)
        #self.next_button.pack(side = RIGHT)

        self.summary = Label(self.top_right_frame, text = self.summary_text)
        self.summary.pack(side = RIGHT)
        
        
        self.middle_frame = GenerationPage.draw_color_mapped_array(self.middle_frame,
                                                                   world.map,
                                                                   GenerationPage.WORLD_COLOR_MAP)
        
        best_travel_map = self.build_travel_array(0)
        mid_travel_map = self.build_travel_array(int(len(self.generation.individuals) / 2))
        worst_travel_map = self.build_travel_array(-1)

        self.bottom_left_frame = GenerationPage.draw_color_mapped_array(self.bottom_left_frame,
                                                                        best_travel_map,
                                                                        GenerationPage.TRAVEL_COLOR_MAP)

        self.bottom_mid_frame = GenerationPage.draw_color_mapped_array(self.bottom_mid_frame ,
                                                                       mid_travel_map,
                                                                        GenerationPage.TRAVEL_COLOR_MAP)

        self.bottom_right_frame= GenerationPage.draw_color_mapped_array(self.bottom_right_frame,
                                                                       worst_travel_map,
                                                                        GenerationPage.TRAVEL_COLOR_MAP)


        self.pack()
        self.top_frame.pack()
        self.top_left_frame.pack(side = LEFT)
        self.top_right_frame.pack(sid = RIGHT)
        self.middle_frame.pack(side = BOTTOM)
        self.bottom_frame.pack(side = BOTTOM)
        self.bottom_left_frame.pack(side = LEFT)
        self.bottom_mid_frame.pack(side = LEFT)
        self.bottom_right_frame.pack(side = LEFT)

        
        GenerationPage.GENERATIONS.append(self)
        self.tkraise()
        GenerationPage.ROOT.mainloop()

    def initialize_header(self):
        return "Generation " + str(self.gnr_count)

    def initialize_sumary(self):
        summary = "Board Shape: " + str(World.SHAPE) + "\n"
        summary += "Food Number: " + str(World.NUM_OF_FOOD) + "\n"
        summary += "Number Of Individuals: " + str(self.generation.NUM_OF_INDIVIDUALS) + "\n"
        summary += "Average Eaten Food: " + str(self.generation.average) + "\n"
        summary += "Maximum Eaten Food: " + str(self.generation.individuals[0].eaten_food)
        return summary

    def click_prev_button(self):
        if self.gnr_count == 0:
            return
        else:
            self.pack_forget()
            GenerationPage.CURRENT_FRAME_INDEX = self.gnr_count - 1
            GenerationPage.GENERATIONS[GenerationPage.CURRENT_FRAME_INDEX].pack()
            GenerationPage.GENERATIONS[GenerationPage.CURRENT_FRAME_INDEX].tkraise()
            

    def click_next_button(self):
        if self.gnr_count == len(GenerationPage.GENERATIONS) - 1:
            new_gnr = Generation(world = self.world, ancestor_individuals = self.generation)
            self.pack_forget()
            new_frame = GenerationPage(self.world, new_gnr, self.gnr_count + 1)
            GenerationPage.GENERATIONS.append(new_frame)
        else:
            self.pack_forget()
        GenerationPage.CURRENT_FRAME_INDEX += 1
        GenerationPage.GENERATIONS[GenerationPage.CURRENT_FRAME_INDEX].pack()
        GenerationPage.GENERATIONS[GenerationPage.CURRENT_FRAME_INDEX].tkraise()
        
    @staticmethod
    def draw_color_mapped_array(frame, array, color_map):
        for i in range(array.shape[0] + 1):
            for j in range(array.shape[1] + 1):
                if i == 0 or j == 0 or i == array.shape[0] or j == array.shape[1]:
                    canvas = Canvas(frame,
                                bg = 'black',
                                height = array.shape[0],
                                width = array.shape[1]).grid(row = i, column = j)
                else:
                    canvas = Canvas(frame,
                                    bg = color_map[array[i, j]],
                                    height = array.shape[0],
                                    width = array.shape[1]).grid(row = i, column = j)
        return frame

    def build_travel_array(self, ind_index):
        travel_map = np.array(self.world.map)
        for pos in self.generation.individuals[ind_index].positions:
            if self.world.map[pos[0], pos[1]] == 0:
                travel_map[pos[0], pos[1]] = 2
            else:
                travel_map[pos[0], pos[1]] = 3
        return travel_map
        
