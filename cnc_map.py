import pygame as pg

from cnc_config import Config
from cnc_herbs import *


class Map:
    def __init__(self):

        self.__path = []
        self.__distance = [0, 0]
        self.__bottle = [10, 0]
        self.surface = pg.Surface((Config.MAP_WIDTH, Config.MAP_HEIGHT))
        self.rect = self.surface.get_rect()
        self.__originX = Config.MAP_WIDTH / 2
        self.__originY = Config.MAP_HEIGHT / 2

        self.bottle_pic = pg.image.load('IngamePic/bottle.png')
        self.bottle_pic = pg.transform.scale(self.bottle_pic, (30, 36))

        self.bottleShad = pg.image.load('IngamePic/BottleShadow.png')
        self.bottleShad = pg.transform.scale(self.bottleShad, (30, 36))

    def get_len_path(self):
        return len(self.__path)

    def get_distance(self):
        return [int(self.__distance[0]), int(self.__distance[1])]

    def get_position(self, coordinate: tuple[float, float], mod_x: float = 0, mod_y: float = 0):
        return (self.__originX + coordinate[0] + mod_x,
                self.__originY - coordinate[1] + mod_y)

    def get_origin(self):
        return self.__originX, self.__originY

    def get_bottle_pos(self, mod_x=0, mod_y=0):
        return self.get_position(self.__bottle, mod_x=mod_x, mod_y=mod_y)

    def get_path_line(self):
        bottle = self.get_bottle_pos()
        line = [[bottle[0], bottle[1]]]
        for i in range(len(self.__path)):
            line.append([line[i][0] + self.__path[i][0], line[i][1] - self.__path[i][1]])
        return line

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

    def move_map(self, key):
        factor_x = Config.FACTOR_x * 2
        if key[pg.K_w]:
            self.__originY += factor_x
        if key[pg.K_s]:
            self.__originY -= factor_x
        if key[pg.K_a]:
            self.__originX += factor_x
        if key[pg.K_d]:
            self.__originX -= factor_x

    def add_herb(self, herb: Herb):
        # print(herb.path())
        self.__path.extend(herb.path)

    def move_along(self):
        if len(self.__path) > 0:
            path = self.__path.pop(0)
            self.__bottle[0] += path[0]
            self.__distance[0] += 1
            self.__bottle[1] += path[1]
            self.__distance[1] += 1
            # print(path)

    def find_distance_btw(self, pos: tuple[float, float]):
        return ((self.__bottle[0] - pos[0]) ** 2 + (self.__bottle[1] - pos[1]) ** 2) ** 0.5

    def done_brewing(self):
        # check all the position
        for potion, pos in Config.POTION_POS.items():
            dis = self.find_distance_btw(pos)
            if dis <= 3:
                print(potion, 3)
            elif dis <= 5:
                print(potion, 2)
            elif dis <= 25:
                print(potion, 1)
            else:
                pass
