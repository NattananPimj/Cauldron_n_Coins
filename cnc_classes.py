import pygame as pg

from cnc_config import Config
from cnc_herbs import *

pg.init()


class Map:
    def __init__(self):

        self.__path = []
        self.__distance = 0
        self.__bottle = [0, 0]
        self.__originX = (Config.MAP_WIDTH/2) + ((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2)
        self.__originY = Config.MAP_HEIGHT/2 + (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 4

    def get_position(self, coordinate: tuple[float, float], mod_x: float = 0, mod_y: float = 0):
        return (self.__originX + coordinate[0] + mod_x,
                self.__originY - coordinate[1] + mod_y)

    def get_origin(self):
        return self.__originX, self.__originY

    def get_bottle_pos(self):
        return self.get_position(self.__bottle)

    def back_to_origin(self):
        factor_x = Config.FACTOR_x
        if self.__bottle[0] == 0:
            h = 0
            k = factor_x
        else:
            slope = abs(self.__bottle[1] / self.__bottle[0])
            h = factor_x
            k = slope * factor_x

        if self.__bottle[0] >= 0:
            self.__bottle[0] -= h
        else:
            self.__bottle[0] += h

        if self.__bottle[1] >= 0:
            self.__bottle[1] -= k
        else:
            self.__bottle[1] += k




class Drawer:
    def __init__(self, m: Map):
        self.__gameinfo = None
        self.__screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.__mapsize = pg.Rect((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                                 (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 4,
                                 Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.__screen.fill(Config.COLOR['background'])
        self.__clock = pg.time.Clock()
        self.__map = m

    def draw_brewing_screen(self):
        self.__screen.fill((Config.COLOR['background']))
        pg.draw.rect(self.__screen, (Config.COLOR['black']), self.__mapsize, width=2)
        # origin
        pg.draw.circle(self.__screen, (Config.COLOR['black']), self.__map.get_position((0, 0)), 10, width=2)
