import pygame, sys, math, random
from Config import Config
from Paiter import Painter
from Ant_cell import Ant_cell
from Cell_Manager import Cell_Manager


class Ant_nest(object):
    def __init__(self, x_y, id, radius=5, energy=10000):
        self.x_y = x_y
        self.radius = radius
        self.id = id
        self.energy = energy
        self.ant_id = 0

        self.New()

    def New(self):
        Painter.circle(Config.Bright_smt, self.x_y, self.radius)

    def Act(self):
        # if True:
        #     return
        saving_energy = Config.s_data["ant_cost"] + Cell_Manager.get_acell_count() * 10
        # print("self.energy", self.energy)
        if self.energy > saving_energy:
            if Cell_Manager.get_acell_count() < Config.s_data["antcells_limit"]:
                self.create_ant()

        for ant in Cell_Manager.get_acell_data():
            if ant.get_energy() < 0:
                ant.death()
                Cell_Manager.remove_acell(ant)
                continue
            if ant.get_pos() == self.x_y:
                self.energy += ant.give_energy()
                ant.set_target(self.get_target())
                ant.change_state("s")

            if ant.get_energy() > Config.s_data["ant_cost"] * 5.5:  # *2.5:
                ant.set_target(self.x_y)
                ant.change_state("b")
            ant.Act()

        Cell_Manager.add_anest(self)

    def get_target(self):
        n = Cell_Manager.get_acell_count() + 1
        Spawn_Lenght = Config.W_w * 2 + Config.W_h * 2
        step = Spawn_Lenght / n
        perimeter = Config.W_w * 2 + Config.W_h * 2
        # step =random.randint(0, perimeter)
        # x, y = Ant_nest.blight_starting_pos(step, n)
        # x = random.randint(0, Config.W_w)
        # y = random.randint(0, Config.W_h)
        x, y = Ant_nest.ant_starting_target()
        # print("get_target", (x, y))
        return (x, y)

    # @staticmethod
    # def blight_starting_pos(step, n):
    #     off_set = 1
    #     l = step * n
    #     if l <= Config.W_w - off_set * 2:
    #         print("1")
    #         x, y = l, 0 + off_set
    #     elif l <= Config.W_w + Config.W_h - off_set * 2:
    #         print("2")
    #         x, y = Config.W_w - off_set, l - Config.W_w
    #     elif l <= Config.W_w * 2 + Config.W_h - off_set * 2:
    #         print("3")
    #         x, y = Config.W_w * 2 + Config.W_h - l - off_set, Config.W_h - off_set
    #     else:
    #         print("4")
    #
    #
    #
    #
    #         x, y = 0 + off_set, Config.W_w * 2 + Config.W_h * 2 - l + off_set
    #     print("step, n = ", step, n)
    #     print("x,y = ", x, y)
    #     return x, y

    @staticmethod
    def ant_starting_target():
        off_set = 1
        perimeter = Config.W_w * 2 + Config.W_h * 2
        l = random.randint(off_set, perimeter)
        if l <= Config.W_w - off_set * 2:
            # print("1")
            x, y = l, 0 + off_set
        elif l <= Config.W_w + Config.W_h - off_set * 2:
            # print("2")
            x, y = Config.W_w - off_set, l - Config.W_w
        elif l <= Config.W_w * 2 + Config.W_h - off_set * 2:
            # print("3")
            x, y = Config.W_w * 2 + Config.W_h - l - off_set, Config.W_h - off_set
        else:
            # print("4")
            x, y = 0 + off_set, Config.W_w * 2 + Config.W_h * 2 - l + off_set
        # x = random.randint(0, x)
        # y = random.randint(0, y)
        # print("step, n = ", step, n)
        # print("x,y = ", x, y)
        return x, y

    def create_ant(self):
        self.energy += -Config.s_data["ant_cost"]
        ant = Ant_cell(self.x_y, self.get_target(), self.ant_id, energy=Config.s_data["ant_cost"], state='s')
        Cell_Manager.add_acell(ant)
        self.ant_id += 1
