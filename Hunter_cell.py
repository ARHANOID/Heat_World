import  math, random
from Config import Config
from Paiter import Painter
from Cell_Manager import Cell_Manager
from Life_cell import Life_cell

class Hunter_cell(Life_cell):

    def __init__(self, x_y, id, energy=0):
        super().__init__(x_y, id, energy)
        self.target_pos = None
        self.color = Config.Bright_blue[2]
        self.speed = 1
        self.pre_color = (0,0,0)
        self.color_power = Config.s_data["hcolor_power"]

        Cell_Manager.add_hcell(self)
        Cell_Manager.remove_lcell(self)

    def death(self):
        # red = (self.color * self.color_power + self.energy) % 255
        # green = (self.color * self.color_power + self.energy) // 255
        red = self.color * self.color_power + self.energy
        if red > 255:
            red = 255
        # red = 0
        green = 0
        Painter.dot((red, green, 0), self.x_y)
        Cell_Manager.remove_hcell(self)

    def feed(self, food):
        self.target_pos = None
        self.hopless = 0
        self.pre_color = (0, 0, 0)
        Painter.dot(self.pre_color, self.x_y)
        self.color += food // self.color_power
        self.energy += food % self.color_power

        if self.energy >= self.color_power:
            self.color += 1
            self.energy += - self.color_power
        if self.color >= 255:
            self.color = Config.Bright_blue[2]
            return 2
        else:
            return 1

    def direction_finder(self, x, y):
        color = Painter.get_dot_color((x, y))
        # print("direction_finder", color)
        energy = color[0] + color[1] * Config.s_data["color_power"] + \
                 color[2] * Config.s_data["color_power"] * Config.s_data["hcolor_power"]
        # if energy > 255*255:
        #     energy = 0
        return energy

    def move(self):
        if self.target_pos is None:
            self.target_pos = Cell_Manager.get_nearest(self.x_y)
        x_target, y_target = self.target_pos
        x_start, y_start = self.x_y
        dx = x_start - x_target
        dy = y_start - y_target

        # if dx == dy == 0:
        #     return False

        if abs(dx) > self.speed:
            x_new = int(x_start - self.speed * math.copysign(1, dx))
        else:
            x_new = x_target
        if abs(dy) > self.speed:
            y_new = int(y_start - self.speed * math.copysign(1, dy))
        else:
            y_new = y_target

        if Cell_Manager.is_hcell_here((y_new, y_new)):
            return 1
        state = 1
        cell = None
        if (x_new == x_target and y_new == y_target) or (Cell_Manager.is_acell_here((y_new, y_new))):
            cell = Cell_Manager.get_cell_from_pos((x_new, y_new))

            if cell is not None:
                energy = cell.consumed()
                state = self.feed(energy)

            else:
                # self.target_pos = Cell_Manager.get_random_lcell_pos()
                self.target_pos = None

        Painter.dot(self.pre_color, self.x_y)

        self.pre_pos = self.x_y
        self.x_y = (x_new, y_new)
        # Cell_Manager.chenge_hc_pos(self.pre_pos, self.x_y)
        self.pre_color = Painter.get_dot_color(self.x_y)
        self.pre_color = (self.pre_color[0],self.pre_color[1],0)
        Painter.dot((0, 0, self.color % 255), (self.x_y))



        # print("2")
        return state

    def hibernation(self):
        self.energy += 1
        return 1


    def act(self):
        self.spending()
        self.spending()

        if self.color <= 0:
            return 0

        if self.hopeless > Config.s_data["hopeless"]*7:
            self.target_pos = None
            if Cell_Manager.get_lcell_count() > 30:
                if Cell_Manager.get_hcell_count() > Cell_Manager.get_lcell_count() / Config.s_data["hcells_limit"]:
                    n = random.randint(0, 4)
                    if n == 1:
                        return 0
                    else:
                        self.target_pos = Cell_Manager.get_random_lcell_pos()
            else:
                # self.target_pos = Cell_Manager.get_random_lcell_pos()
                return self.hibernation()

            self.hopeless = 0

        return self.move()

