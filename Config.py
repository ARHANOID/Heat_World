class Config():
    W_w = 1920#800#1920#1024
    W_h = 1080#600#1080#840


    center_width = W_w // 2
    center_height = W_h // 2

    s_data = {"color_power": 25,
              "hcolor_power": 255,
              "lcells_limit": 6000,
              "hcells_limit": 15,
              "antcells_limit": 5000,
              "radiation_level": 100,
              "radiation_power": 25,
              "hopeless": 25,
              "starting_heat": 25,
              "ant_cost": 200,
              "ant_str": 50,
              "FPS": 9000}

    Bright_green = (0, 85, 0)
    Bright_blue = (0, 0, 85)
    Bright_smt = (0, 185, 185)
    Bright_smt = (0, 55, 55)
    Shine_smt = (0, 155, 155)
    font_size = int(W_w/50)

    right = ( 1, 0)
    up = (0,  1)
    left = (-1, 0)
    douw = (0, -1)
    Direction = ((right, up, left, douw),(up, left, douw, right),(left, douw, right, up), (douw, right, up, left))




    @staticmethod
    def screen_w(x):
        return int(x*Config.W_w/34)
    @staticmethod
    def screen_h(x):
        return int(x*Config.W_h/28)


