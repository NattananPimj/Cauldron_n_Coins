import pygame as pg
from cnc_config import Config


class Map:
    def __init__(self):
        self.map = pg.Rect((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                           (Config.SCREEN_HEIGHT - Config.SCREEN_HEIGHT) / 2,
                           Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.__path = []
        self.__distance = 0
        self.__bottle = [0, 0]

    @staticmethod
    def get_position(coordinate: tuple[float, float], mod_x: float = 0, mod_y: float = 0):
        return (Config.ORIGIN_X + coordinate[0] + mod_x,
                Config.ORIGIN_Y - coordinate[1] + mod_y)

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


class Herb:
    def __init__(self, name, direction, func, file, x, y):
        self.name = name
        self.direction = direction
        self.func = func
        self.picture = file
        self.size_x = x
        self.size_y = y
        self.factor_x = []
        self.factor_y = []


class Horizontal_Herb(Herb):
    # E or W
    def __init__(self, name, direction, func, file, x, y):
        super().__init__(name, direction, func, file, x, y)
        if self.direction == 'E':
            self.factor_x = [i / 10 for i in range(x * 10)]
        if self.direction == 'W':
            self.factor_x = [-i / 10 for i in range(x * 10)]

    def get_path(self, distance):
        path = []
        if distance < len(self.factor_x):
            for i in range(distance, len(self.factor_x)):
                path.append([self.factor_x[0] / 10, self.func(self.factor_x[i]) - self.factor_x[i - 1]])
        return path

    def get_coordinate(self, distance):
        line = []
        if distance < len(self.factor_x):
            for i in range(distance, len(self.factor_x)):
                line.append([self.factor_x[i], self.func(self.factor_x[i]) + self.size_y / 2])
        return line
