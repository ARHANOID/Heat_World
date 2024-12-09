from Config import Config
import random


s_lcell_data = []
s_hcell_data = []
s_acell_data = []

l_lcell_pos = set()
l_hcell_pos = set()
l_acell_pos = set()

s_anest_data = []

test_spicke = []
test_spicke.append(True)



class Cell_Manager():
    @staticmethod
    def add_lcell(cell):
        s_lcell_data.append(cell)

    @staticmethod
    def add_hcell(cell):
        s_hcell_data.append(cell)

    @staticmethod
    def add_acell(cell):
        s_acell_data.append(cell)

    @staticmethod
    def add_anest(nest):
        s_anest_data.clear()
        s_anest_data.append(nest)

    @staticmethod
    def remove_lcell(cell):
        s_lcell_data.remove(cell)

    @staticmethod
    def remove_hcell(cell):
        s_hcell_data.remove(cell)

    @staticmethod
    def remove_acell(cell):
        s_acell_data.remove(cell)

    @staticmethod
    def is_hcell_here(x_y):
        if x_y in l_hcell_pos:
            return True
        return False

    @staticmethod
    def change_test_state():
        flag = test_spicke.pop(0)
        test_spicke.append(not flag)

    @staticmethod
    def get_test_state():
        return test_spicke[0]

    @staticmethod
    def is_lcell_here(x_y):
        if x_y in l_lcell_pos:
            return True
        return False

    @staticmethod
    def is_acell_here(x_y):
        if x_y in l_acell_pos:
            return True
        return False

    @staticmethod
    def is_cell_here(x_y):
        if x_y in l_lcell_pos:
            return True
        if x_y in l_hcell_pos:
            return True
        if x_y in l_acell_pos:
            return True
        return False

    @staticmethod
    def get_last_cell_id():
        return s_lcell_data[-1].id
    @staticmethod
    def get_last_hcell_id():
        return s_hcell_data[-1].id
    @staticmethod
    def get_lcell_count():
        return len(s_lcell_data)
    @staticmethod
    def get_hcell_count():
        return len(s_hcell_data)
    @staticmethod
    def get_acell_count():
        return len(s_acell_data)
    @staticmethod
    def get_lcell_data():
        return s_lcell_data
    @staticmethod
    def get_hcell_data():
        return s_hcell_data
    @staticmethod
    def get_acell_data():
        return s_acell_data

    @staticmethod
    def get_all_data():
        return s_lcell_data, s_hcell_data, s_acell_data, s_anest_data

    @staticmethod
    def get_lcell_from_pos(x_y):
        for cell in s_lcell_data:
            if x_y == cell.get_pos():
                return cell
        return None
    @staticmethod
    def get_acell_from_pos(x_y):
        for cell in s_acell_data:
            if x_y == cell.get_pos():
                return cell
        return None
    @staticmethod
    def get_cell_from_pos(x_y):
        for cell in s_lcell_data:
            if x_y == cell.get_pos():
                return cell
        for cell in s_acell_data:
            if x_y == cell.get_pos():
                return cell
        return None



    @staticmethod
    def get_random_lcell_pos():
        n = random.randint(0, len(s_lcell_data)-1)
        return s_lcell_data[n].get_pos()

    @staticmethod
    def start_turn():
        # print(" start_turn")
        Cell_Manager.change_test_state()
        Cell_Manager.make_a_set()

    @staticmethod
    def make_a_set():
        l_lcell_pos.clear()
        l_hcell_pos.clear()
        l_acell_pos.clear()

        for elem in s_lcell_data:
            l_lcell_pos.add(elem.get_pos())
        for elem in s_hcell_data:
            l_hcell_pos.add(elem.get_pos())
        for elem in s_acell_data:
            l_acell_pos.add(elem.get_pos())


    @staticmethod
    def get_nearest(x_y):
        x, y = x_y
        minl = 9999999
        for elem in s_lcell_data:
            x1, y1 = elem.get_pos()
            if x1 < 0 or x1 > Config.W_w-1:
                continue
            if y1 < 0 or y1 > Config.W_h-1:
                continue
            l = Cell_Manager.lenght(x, y, x1, y1)
            if minl > l:
                minl = l
                x2, y2 = x1, y1
        return (x2, y2)

    @staticmethod
    def lenght(x1, y1, x2, y2):
        r1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return r1

    @staticmethod
    def load_all_data(lcells, hcells, acells, anest):
        s_lcell_data.clear()
        s_hcell_data.clear()
        s_acell_data.clear()
        s_anest_data.clear()
        for elem in lcells:
            s_lcell_data.append(elem)
        for elem in hcells:
            s_hcell_data.append(elem)
        for elem in acells:
            s_acell_data.append(elem)
        for elem in anest:
            s_anest_data.append(elem)





    pass