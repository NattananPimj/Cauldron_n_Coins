import pygame as pg

from cnc_classes import Map
from cnc_config import Config
import math


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
        self.path = self.get_path
        self.last_pos = [0, 0]
        self.offset = [0, 0]

    def get_path(self):
        return []


class Horizontal_Herb(Herb):
    # E or W
    def __init__(self, name, direction, func, file, x, y):
        super().__init__(name, direction, func, file, x, y)
        if self.direction == 'E':
            self.factor_x = [i / 10 for i in range(x * 10)]
        if self.direction == 'W':
            self.factor_x = [-i / 10 for i in range(x * 10)]
        self.last_pos = [self.factor_x[-1], func(self.factor_x[-1]) - self.size_y / 2]

    def get_path(self):
        path = []
        for i in range(1, len(self.factor_x)):
            path.append([self.factor_x[1], self.func(self.factor_x[i]) - self.func(self.factor_x[i - 1])])
        return path


class Vertical_Herb(Herb):
    # W / S
    def __init__(self, name, direction, func, file, x, y):
        super().__init__(name, direction, func, file, x, y)
        if self.direction == 'N':
            self.factor_y = [(i + 1) / 10 for i in range(y * 10)]
        if self.direction == 'S':
            self.factor_y = [-(i + 1) / 10 for i in range(y * 10)]
        self.last_pos = [func(self.factor_y[-1]) - self.size_x / 2, self.factor_y[-1]]

    def get_path(self):
        path = []
        for i in range(1, len(self.factor_y)):
            path.append([self.func(self.factor_y[i]) - self.func(self.factor_y[i - 1]), self.factor_y[1]])
        return path


class HerbManager:
    __HERB_INFO = {
        'Snowy Galangal': {
            'name': 'Snowy Galangal',
            'direction': 'W',
            'func': '',
            'file': '',
            'x': 200,
            'y': 40
        },
        'Dragon Pepper': {

        },
        'Spark Angelica': {
            'name': 'Spark Angelica',
            'direction': 'E',
            'func': lambda x: 10 * math.sin(x / 5),
            'file': '',
            'x': 200,
            'y': 50
        },
        'Ivory Mint':
            {

            },

    }

    def __init__(self, m:Map):
        self.surface = pg.Surface((150, 630))
        self.__map = m

    def add_herb(self, herb_name):
        info = self.__HERB_INFO[herb_name]
        herb = Herb(
            info['name'],
            info['direction'],
            info['func'],
            info['file'],
            info['x'],
            info['y']
        )
        self.__map.add_herb(herb)