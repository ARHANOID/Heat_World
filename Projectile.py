import math
from Paiter import Painter
from Blight_Manager import Blight_Managger

NAVYBLUE = (60, 60, 100)
YELLOW = (255, 255, 0)
RED_1 = (200, 30, 30)


class Projectile(object):

    def __init__(self, destination, current_p, speed=10, radius=3, exp_radius=3 * 20):
        self.current_p = [current_p[0], current_p[1]]
        self.destination = destination
        self.speed = speed
        self.radius = radius
        self.exp_radius = exp_radius

    def act(self):
        # print("Projectile.move",  self.current_p, self.destination)
        Painter.circle(RED_1, (self.current_p[0], self.current_p[1]), self.radius)
        checker = 0
        dx = self.current_p[0] - self.destination[0]
        dy = self.current_p[1] - self.destination[1]

        if abs(dx) > self.speed:
            self.current_p[0] = self.current_p[0] - self.speed * math.copysign(1, dx)
        else:
            checker += 1
            self.current_p[0] = self.destination[0]

        if abs(dy) > self.speed:
            self.current_p[1] = self.current_p[1] - self.speed * math.copysign(1, dy)
        else:
            checker += 1
            self.current_p[1] = self.destination[1]

        if checker == 2:
            return self.explosion()

        Painter.circle(YELLOW, (self.current_p[0], self.current_p[1]), self.radius)

        return None

    def explosion(self):
        Painter.circle(RED_1, (self.current_p[0], self.current_p[1]), self.exp_radius)

        return Blight_Managger.explosion(self.current_p[0], self.current_p[1], self.exp_radius)
