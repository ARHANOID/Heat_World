import pygame, sys, math, random
from pygame.locals import *

# import Projectile
from Projectile import Projectile
from Paiter import Painter
from Blight_Manager import Blight_Managger
from Life_cell import Life_cell
from Hunter_cell import Hunter_cell
from Cell_Manager import Cell_Manager
from Menu import Menu
from Config import Config
from Ant_nest import Ant_nest
from multiprocessing import Process, current_process
import time

step = Config.W_h // 6
zero = '0'
cross = 'X'
mass = [zero, cross]

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_bl = (30, 200, 40)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

Projectile_speed = 3


def drawscore(x):
    return


"c:\Саша\programming\Pycharming\Heat_World\main.py"



def Anest_act(nest):
    nest.Act()


def Painter_act(smt):
    Painter.Heat_act()


def LCell_act(new_cells_temp):
    for Cell in Cell_Manager.get_lcell_data():
        act = Cell.act()
        if act == 0:
            Cell.death()
        elif act == 2:
            x1, x2 = Cell.multiply()
            new_cells_temp.append(x1)

def my_shiny_new_decorator(function_to_decorate, *args):
    def the_wrapper_around_the_original_function(*args):
        print("Я - код, который отработает до вызова функции")
        function_to_decorate(args)  # Сама функция
        print("А я - код, срабатывающий после")

    return the_wrapper_around_the_original_function


def my_shiny_new_decorator2(function_to_decorate, *args):
    def the_wrapper_around_the_original_function(*args):
        print("Я -1")
        function_to_decorate(args)  # Сама функция
        print("А я - 2")

    return the_wrapper_around_the_original_function


def my_shiny_new_decorator3(function_to_decorate, *args):
    def the_wrapper_around_the_original_function(*args):
        print("Я - 3")
        function_to_decorate(args)  # Сама функция
        print("А я - 4")

    return the_wrapper_around_the_original_function

def HCell_act(new_cells_temp):
    for HCell in Cell_Manager.get_hcell_data():
        act = HCell.act()
        if act == 0:
            HCell.death()
        elif act == 2:
            x1, x2 = HCell.multiply()
            new_cells_temp.append(x1)


def main(level, score):
    sys.setrecursionlimit(50000)
    Painter.initialize()
    Print_time_interval = 10000

    Game_time = 0

    amo_in_air = []

    Ant_nest_1 = Ant_nest((Config.screen_w(30), Config.screen_h(22)), 0, 1)

    Life_cell_id = 0
    Life_cell((Config.screen_w(15), Config.screen_h(13)), Life_cell_id, 300)
    Life_cell_id += 1
    Hunter_cell((Config.W_w, Config.W_h), Life_cell_id, 1000)
    Life_cell_id += 1

    Painter.smt()

    tasks = []
    new_cells = []
    new_hcells = []
    tasks.append((Painter_act, None, "Painter_act"))
    tasks.append((Anest_act, Ant_nest_1, "Ant_nest"))
    tasks.append((LCell_act, new_cells, "LCell_act"))
    tasks.append((HCell_act, new_hcells, "HCell_act"))

    while True:
        Painter.lock_display()
        new_cells.clear()
        new_hcells.clear()


        for i in range(Config.s_data["radiation_level"]):
            x_a = (random.randint(0, Config.W_w), random.randint(0, Config.W_h))
            Painter.Target_heated(x_a, Config.s_data["radiation_power"])

        Painter.Target_heated((Config.screen_w(4), Config.screen_h(22)), 10 * Config.s_data["radiation_power"])
        Painter.Target_heated((Config.screen_w(16.5), Config.screen_h(12.5)), 10 * Config.s_data["radiation_power"])
        Painter.Target_heated((Config.screen_w(30), Config.screen_h(3)), 10 * Config.s_data["radiation_power"])
        Painter.Target_heated((Config.screen_w(4), Config.screen_h(4)), 10 * Config.s_data["radiation_power"])

        mouseClicked = False

        if Game_time % Print_time_interval == 0:
            print("Game_time", Game_time)

        Cell_Manager.start_turn()


        for elem in tasks:
            elem[0](elem[1])

        for proj in amo_in_air:
            result = proj.act()
            if result is not None:
                score += result
                amo_in_air.remove(proj)

        for position in new_cells:
            Life_cell_id += 1
            Life_cell((position), Life_cell_id)
        for position in new_hcells:
            Life_cell_id += 1
            Hunter_cell((position), Life_cell_id)

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif (event.type == KEYUP and event.key == K_F10):
                Menu.save_screen("Main_screen")
                Menu.Open()
                Menu.load_screen("Main_screen")

        if mouseClicked:
            print("mouseClicked", event.pos)
            expo = Projectile(event.pos, (Config.center_height, Config.center_width))
            amo_in_air.append(expo)

        Game_time += 1
        Painter.update()


if __name__ == '__main__':
    main(1, 0)
