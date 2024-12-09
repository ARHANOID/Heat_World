import pygame, sys, math, random
# from pygame.locals import *
from Config import Config

s_Ticked_dots = set()
s_Heat = {}
Name = 'Heat World'

step = Config.W_h // 6
zero = '0'
cross = 'X'
mass = [zero, cross]

START = (Config.s_data["starting_heat"], 0, 0)

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

Projectile_speed = 3

class Painter(object):
    def __init__(self):
        pass
    @staticmethod
    def initialize():
        global FPSCLOCK, DISPLAYSURF
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((Config.W_w, Config.W_h))
        pygame.display.set_caption(Name)
        Painter.game_start()



    @staticmethod
    def game_start():
        DISPLAYSURF.fill(START)
        # Painter.smt()

        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.center_width - int(step * 1.0), Config.W_h / 1.8),
        #                  (Config.center_width - int(step * 1.0), Config.W_h / 2.2), 5)
        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.W_w / 2.9, Config.center_height + int(step * 0.34)),
        #                  (Config.W_w / 2.6, Config.center_height + int(step * 0.34)), 5)
        #
        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.center_width, Config.W_h / 1.8),
        #                  (Config.center_width, Config.W_h / 2.2), 5)
        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.W_w / 2.9 + int(step * 1.0), Config.center_height + int(step * 0.34)),
        #                  (Config.W_w / 2.6 + int(step * 1.0), Config.center_height + int(step * 0.34)), 5)
        #
        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.center_width + int(step * 1.0), Config.W_h / 1.8),
        #                  (Config.center_width + int(step * 1.0), Config.W_h / 2.2), 5)
        # pygame.draw.line(DISPLAYSURF, ORANGE, (Config.W_w / 2.9 + int(step * 2.0), Config.center_height + int(step * 0.34)),
        #                  (Config.W_w / 2.6 + int(step * 2.0), Config.center_height + int(step * 0.34)), 5)

    @staticmethod
    def drawItems(item, x, y, size = Config.W_w // 25):
        fontObj = pygame.font.Font('freesansbold.ttf',size)
        textSurfaceObj = fontObj.render(item, True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    @staticmethod
    def update():
        DISPLAYSURF.unlock()
        pygame.display.update()
        s_Ticked_dots.clear()
        FPSCLOCK.tick(Config.s_data["FPS"])

    @staticmethod
    def circle(color,center,radius):
        pygame.draw.circle(DISPLAYSURF, color, center, radius)

    @staticmethod
    def dot(color, center):
        DISPLAYSURF.set_at(center,color)

    @staticmethod
    def line(color, start, finish, wide):
        pygame.draw.line(DISPLAYSURF, color, start, finish, wide)

    @staticmethod
    def T_inc(x_y,t):
        if x_y in s_Ticked_dots:
            # print("0",t)
            return t
        x, y = x_y
        # if x < 0 or x >= Config.W_w or y < 0 or y >= Config.W_h:
        #     # print("1", t)
        #     return t

        s_Ticked_dots.add(x_y)

        # print("x_y", x_y)
        r, g, b, h = DISPLAYSURF.get_at(x_y)
        r+= t
        t = 0
        if r > 255:
            r = int(r/5)
            Painter.Dict_add((x, y+1), r)
            Painter.Dict_add((x, y-1), r)
            Painter.Dict_add((x+1, y), r)
            Painter.Dict_add((x-1, y), r)
            # r+= t
            # t = 0
        if r > 255:
            r, g = 0, g + int(1+ r/255)
        if g > 255:
            g, b = 0, b + int(1+ g/255)
        if b > 255:
            print("WTF. No heat could be add. World ERROR")
            b = 255
        result = (r,g,b,h)
        # print("",x_y,result)
        # Painter.circle(result, x_y, 1)
        Painter.dot(result, x_y)

        return t

    @staticmethod
    def get_dot_color(x_y):
        x,y = x_y
        if x < 0 or x >= Config.W_w or y < 0 or y >= Config.W_h:
            return (0,0,0,255)
        return DISPLAYSURF.get_at(x_y)

    @staticmethod
    def Dict_add(x_y, t):
        x, y = x_y
        if x < 0:
            x += 2
        if x >= Config.W_w:
            x += -2
        if y < 0:
            y += 2
        if y >= Config.W_h:
            y += -2
        x_y = (x, y)
        if x_y not in s_Heat.keys():
            s_Heat[x_y] = t
        else:
            s_Heat[x_y] += t
    @staticmethod
    def Target_heated(x_y, t):
        Painter.Dict_add(x_y, t)
        # Painter.T_inc(x_y, t)

    @staticmethod
    def Heat_act():
        Past_heat=s_Heat.copy()
        for x_y, t in Past_heat.items():
            s_Heat.pop(x_y)
            t = Painter.T_inc(x_y, t)
            if t > 0:
                Painter.Dict_add(x_y, t)

    @staticmethod
    def save_display():
        format1 = "RGB"
        # pre_sur = pygame.Surface.copy()
        # return DISPLAYSURF.copy()

        # pygame.pixelcopy.surface_to_array(array,DISPLAYSURF)
        # return pygame.PixelArray(DISPLAYSURF)
        return pygame.image.tostring(DISPLAYSURF, format1)

    @staticmethod
    def lock_display():
        # pre_sur = pygame.Surface.copy()
        return DISPLAYSURF.lock()

    @staticmethod
    def unlock_display():
        # pre_sur = pygame.Surface.copy()
        return DISPLAYSURF.unlock()

    @staticmethod
    def load_display(saves):
        size = (Config.W_w, Config.W_h)
        format1 = "RGB"
        surf = pygame.image.fromstring(saves, size, format1)
        DISPLAYSURF.blit(surf, (0, 0))
        # pygame.image.load(img)
        # pygame.Pixelrray.make_surface()
        # surf = pygame.pixelcopy.array_to_surface(DISPLAYSURF, saves)
        # DISPLAYSURF.blit(surf, (0,0))
        # pygame.display.set_caption(Name)

    @staticmethod
    def derorrator_first(f):
        print("Before")
        val = f()
        print("After")
        return val

    @staticmethod
    # @derorrator_first
    def smt():
        ar = Painter.Create_arrey()
        ar2 = Painter.My_first_sort(ar)
        print("surted_arrey [", end='')
        for i in range(len(ar2)):
            print(ar2[i], ",", end='')
        print("]")
        flag = Painter.sort_checker(ar2)
        print(flag)
    @staticmethod
    def sort_checker(arrey):
        flag = True
        for i in range(1, len(arrey), -1):
            if arrey[i] < arrey[i-1]:
                flag = False
                break
        for i in range(0, len(arrey)-1):
            if arrey[i] > arrey[i+1]:
                flag = False

        return flag


    @staticmethod
    def Create_arrey():
        size = 100
        unsorted_arrey = []
        for i in range(size):
            n = random.randint(0, size)
            unsorted_arrey.append(n)
        print("unsorted_arrey", unsorted_arrey)
        return unsorted_arrey

    @staticmethod
    def My_first_sort(arrey):
        min_element = 9999999999
        min_index = 0
        for j in range(len(arrey)):
            flag = False
            for i in range(j, len(arrey)):
                if min_element > arrey[i]:
                    min_element = arrey[i]
                    min_index = i
                    flag = True
            if flag:
                arrey[j], arrey[min_index] = arrey[min_index], arrey[j]
                min_element = 9999999999

        return arrey







