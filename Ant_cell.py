import pygame, sys, math, random
from Config import Config
from Paiter import Painter
from Cell_Manager import Cell_Manager




class Ant_cell(object):
    def __init__(self, x_y, target, id, energy = 100, state = 's'):
        self.x_y = x_y
        self.home = x_y
        self.target = target
        # self.pre_pos = x_y
        self.cargo = 0
        self.color = energy
        self.energy = energy
        self.id = id
        self.state = state



    def change_state(self, x = 's'):

        self.state = x
    def search(self):
        self.spending()
        if self.x_y != self.target:
            # print(self.target)
            x_target, y_target = self.target
            x_start, y_start = self.x_y
            dx = x_start - x_target
            dy = y_start - y_target

            x = int(self.x_y[0] - random.randint(0, 1) * math.copysign(1, dx))
            y = int(self.x_y[1] - random.randint(0, 1) * math.copysign(1, dy))


            food = self.energy_counter((x, y))
            self.feed(food)
            self.move((x, y))
        else:
            self.change_state("b")



    def back(self):
        self.search()

    def repair(self):
        pass
    def get_energy(self):
        return self.energy
    def get_pos(self):
        return self.x_y
    def set_target(self, target):
        self.target = target
    def give_energy(self):
        # print("give_energy self.energy", self.energy)
        if self.energy > Config.s_data["ant_cost"]:
            dif = self.energy - Config.s_data["ant_cost"]
            self.energy += -dif
            # print("give_energy self.energy, dif",self.energy, dif)
            return dif
        return 0

    def spending(self):
        self.energy += -1
        # self.color = min(self.energy, 255)
        self.color = self.energy

    def move(self, target):
        Painter.dot((0, self.color % 255, self.color % 255), target)
        Painter.dot((0, 0, 0), self.x_y)
        self.pre_pos = self.x_y
        self.x_y = target

        if Cell_Manager.is_lcell_here(self.x_y):
            lcell_str = 100 - Config.s_data["ant_str"]
            cell = Cell_Manager.get_lcell_from_pos(self.x_y)
            if cell is not None:
                l_str = cell.get_color() * lcell_str / 100
                a_str = self.color * Config.s_data["ant_str"] / 100
                perimeter = l_str + a_str
                result = random.randint(0, int(perimeter))
                if result < l_str:
                    cell.feed(self.consumed())
                else:
                    self.feed(cell.consumed())

        return True

    def feed(self, food):
        # print("feed food", food)
        self.energy += food
        # print("feed self.energy", self.energy)

    def energy_counter(self, x_y):
        color = Painter.get_dot_color(x_y)
        energy = color[0]
        return energy
    def death(self):
        Painter.dot((0, 0, 0), self.x_y)
        # Cell_Manager.remove_cell(self)
    def consumed(self):
        food = self.color + self.energy
        self.color = 0
        self.energy = 0

        self.death()
        return food

    def Act(self):
        if self.state == "s":
            self.search()
        if self.state == "b":
            # print("self.state == b", self.target, self.x_y)
            self.back()
        if self.state == "r":
            self.repair()