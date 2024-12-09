import math
from Paiter import Painter
from Config import Config
s_data = {}

class Blight_data():
    def __init__(self, x, y, power, key, color):
        self.id = key
        self.power = power
        self.body = []
        self.body.append((x, y))
        self.color =  color

    def set_grow(self, x, y):
        self.body.append((x,y))

    def update_grow(self, x,y):
        self.body.pop(-1)
        self.body.append((x,y))

class Blight_Managger(object):
    def __init__(self):
        pass
    @staticmethod
    def set_new(x, y, power, color):
        key = len(s_data)
        s_data[key] = Blight_data(x, y, power, key, color)
        print("set_new",key, s_data[key].body)
        return key
    @staticmethod
    def get_blight(key):
        return s_data[key]
    @staticmethod
    def get_count():
        return len(s_data)
    @staticmethod
    def consume(key1, key2):
        bl1 = s_data[key1]
        bl2 = s_data.pop(key2)
        bl1.power = bl1.power + bl2.power
        bl1.body.extend(bl2.body)

    @staticmethod
    def exist(key):
        if key in s_data:
            return True
        else:
            return False
    @staticmethod
    def kill(key):
        s_data.pop(key)
    @staticmethod
    def fing_nearest(key_current):
        flag = False
        target = s_data[key_current]
        if len(s_data) == 1:
            return target.body[-1][0], target.body[-1][1], Config.center_height, Config.center_width, key_current
        r_min = 100500
        for key, blight in s_data.items():
            if key_current == key:
                continue
            # print("key", key, key_current)
            r1 = Blight_Managger.lenght(target.body[-1][0], target.body[-1][1], blight.body[-1][0], blight.body[-1][1])
            if r1 < r_min:
                r_min = r1
                key_min = key
                x_start, y_start, x_res, y_res = target.body[-1][0], target.body[-1][1], blight.body[-1][0], blight.body[-1][1]

            r1 = Blight_Managger.lenght(target.body[-1][0], target.body[-1][1], blight.body[0][0], blight.body[0][1])
            if r1 < r_min:
                r_min = r1
                key_min = key
                x_start, y_start, x_res, y_res = target.body[-1][0], target.body[-1][1], blight.body[0][0], blight.body[0][1]

            r1 = Blight_Managger.lenght(target.body[0][0], target.body[0][1], blight.body[-1][0], blight.body[-1][1])
            if r1 < r_min:
                r_min = r1
                key_min = key
                x_start, y_start, x_res, y_res = target.body[0][0], target.body[0][1], blight.body[-1][0], blight.body[-1][1]
                flag = True

            r1 = Blight_Managger.lenght(target.body[0][0], target.body[0][1], blight.body[0][0], blight.body[0][1])
            if r1 < r_min:
                r_min = r1
                key_min = key
                x_start, y_start, x_res, y_res = target.body[0][0], target.body[0][1], blight.body[0][0], blight.body[0][1]
                flag = True
        if flag:
            target.body.reverse()

        # print("Blight_Managger.fing_nearest", key_current, x_start, y_start, x_res, y_res)
        return x_start, y_start, x_res, y_res, key_min

    @staticmethod
    def act(key):
        if not Blight_Managger.exist(key):
            return False
        bl = Blight_Managger.get_blight(key)

        x_start, y_start, x_res, y_res, key_min = Blight_Managger.fing_nearest(key)
        # print("act",self.id, x_start, y_start, x_res, y_res)
        dx = x_start - x_res
        dy = y_start - y_res

        if dx == dy == 0:
            Blight_Managger.consume(key_min, key)
            return False

        if abs(dx) > bl.power:
            x_new = x_start - bl.power * math.copysign(1, dx)
        else:
            x_new = x_res
        if abs(dy) > bl.power:
            y_new = y_start - bl.power* math.copysign(1, dy)
        else:
            y_new = y_res

        Painter.line(bl.color, (x_start, y_start), (x_new, y_new),3) #3*bl.power)
        bl.set_grow(x_new, y_new)
        return True

    @staticmethod
    def lenght(x1, y1, x2, y2):
        r1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return r1

    @staticmethod
    def lenght_recurce(x,y, r, blight, counter):
        counter += 1*blight.power
        if len(blight.body) == 0:
            Blight_Managger.kill(blight.id)
            return False
        x1, y1 = blight.body.pop(-1)
        r1 = Blight_Managger.lenght(x, y, x1, y1)
        if r1 <= r:
            return Blight_Managger.lenght_recurce(x,y, r, blight, counter)
        else:
            blight.set_grow(x1, y1)
            return True, counter


    @staticmethod
    def explosion(x,y, r):
        points = 0
        for key, blight in s_data.items():
            # print("key", key, key_current)
            r2 = Blight_Managger.lenght(x, y, blight.body[-1][0], blight.body[-1][1])
            if r2 < r:
                flag, points = Blight_Managger.lenght_recurce(x, y, r, blight, points)
                if not flag:
                    break
        return points