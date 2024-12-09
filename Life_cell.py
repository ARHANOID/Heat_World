import pygame, sys, math, random
from Config import Config
from Paiter import Painter
from Cell_Manager import Cell_Manager


class Life_cell(object):
    def __init__(self, x_y, id, energy = 0):
        self.x_y = x_y
        self.pre_pos = x_y
        self.energy = energy
        self.color = Config.Bright_green[1]
        self.id = id
        self.hopeless = 0
        self.color_power = Config.s_data["color_power"]
        self.direction = random.randint(0, 3)
        Cell_Manager.add_lcell(self)

    def direction_finder(self):
        maximum = -1
        direct = Config.Direction[self.direction]
        indexer = -1
        last_index = 0
        for d in direct:
            indexer += 1
            energy = self.energy_counter((self.x_y[0]+d[0], self.x_y[1]+d[1]))
            # print(energy, d)

            if energy > maximum:
                last_index = indexer
                x, y = self.x_y
                maximum = energy
                x, y = self.x_y[0] + d[0], self.x_y[1] + d[1]
        # print("direction_finder", maximum, x,y)
        # print( self.direction , last_index)
        self.direction += last_index
        self.direction = self.direction % 4
        # print(self.direction)
        return maximum, x,y

    def energy_counter(self, x_y):
        color = Painter.get_dot_color(x_y)
        energy = color[0]  # + color[1]*255 + color[2]*255*255
        # if energy > 255:
        #     if Cell_Manager.is_cell_here((x, y)):
        #         energy = -1
        return energy

    def get_pos(self):
        return self.x_y

    def get_color(self):
        return self.color

    def rand_move(self):
        # self.spending()

        x = self.x_y[0] + random.randint(-1,1)
        y = self.x_y[1] + random.randint(-1, 1)
        # if (x,y) == self.pre_pos:
        #     self.hopeless += 1
        #     self.rand_move()
        return (x,y)

    def feed(self, food):
        self.hopeless = 0
        self.color += food // self.color_power
        self.energy += food % self.color_power
        # print("self.color,  self.energy", self.color,  self.energy)
        if self.energy >= self.color_power:
            self.color += 1
            self.energy += - self.color_power
        if self.color >= 255:
            return 2
        else:
            return 1
    def multiply(self):
        # print("multiply"*10)
        self.energy = 0
        self.color = Config.Bright_green[1]
        return (self.x_y[0]+1, self.x_y[1]+1),( self.x_y[0]-1, self.x_y[1]-1)

    def spending(self):
        self.hopeless += 1
        self.energy += -1
        if self.energy < 0:
            self.color += -1
            self.energy += self.color_power

    def move(self,x,y):
        Painter.dot((0, self.color % 255, 0), (x, y))
        Painter.dot((0, 0, 0), self.x_y)
        self.pre_pos = self.x_y
        self.x_y = (x, y)
        # Cell_Manager.chenge_lc_pos(self.pre_pos, self.x_y)
        return True
    def consumed(self):
        food = self.color * self.color_power + self.energy
        self.color = 0
        self.energy = 0

        self.death()
        return food
    def death(self):
        # red = (self.color * self.color_power + self.energy) % 255
        # green = (self.color * self.color_power + self.energy) // 255
        red = self.color * self.color_power + self.energy
        if red > 255:
            red = 255
        green = 0
        Painter.dot((red, green, 0), self.x_y)
        Cell_Manager.remove_lcell(self)

    def act(self):
        self.spending()
        if self.color <= 0:
            return 0
        if self.hopeless > Config.s_data["hopeless"]:
            if Cell_Manager.get_lcell_count() > Config.s_data["lcells_limit"]:
                return 0
            else:
                self.hopeless = 0

        maximum,  x,y = self.direction_finder()
        # if Cell_Manager.is_cell_here((x, y)) or maximum < 1:
        if maximum < 1:
            x, y = self.rand_move()
            self.move(x, y)

            return 1
        else:
            if self.move(x, y):
                return self.feed(maximum)
            else:
                return 1



