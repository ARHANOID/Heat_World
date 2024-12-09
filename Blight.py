import math
from Blight_Manager import Blight_Managger
from Paiter import Painter

GREEN = (30, 200, 40)

class Blight(object):
    def __init__(self, x=0, y=0, power = 1):
        self.id = Blight_Managger.set_new(x,y, power)
        self.speed = power

    def act(self):
        if not Blight_Managger.exist(self.id):
            return False

        self.speed = Blight_Managger.get_power(self.id)
        x_start, y_start, x_res, y_res, key_min = Blight_Managger.fing_nearest(self.id)
        # print("act",self.id, x_start, y_start, x_res, y_res)
        dx = x_start - x_res
        dy = y_start - y_res

        if abs(dx) > self.speed:
            x_new = x_start - self.speed * math.copysign(1, dx)
        else:
            x_new = x_res
        if abs(dy) > self.speed:
            y_new = y_start - self.speed * math.copysign(1, dy)
        else:
            y_new = y_res

        # Painter.circle(GREEN, (x_start, y_start), 1)
        Painter.line(GREEN,(x_start,y_start),(x_new,y_new),5)
        # print("act", x_start, y_start)
        Blight_Managger.update_2(self.id, x_new, y_new)
        if dx == dy == 0:
            Blight_Managger.consume(key_min, self.id)
            return False
        return True