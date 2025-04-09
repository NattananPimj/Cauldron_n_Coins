import pygame as pg

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
        if 'E' in self.direction:
            self.factor_x = [i / 10 for i in range(x * 10)]
        if 'W' in self.direction:
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
        if 'N' in self.direction:
            self.factor_y = [(i + 1) / 10 for i in range(y * 10)]
        if 'S' in self.direction:
            self.factor_y = [-(i + 1) / 10 for i in range(y * 10)]
        self.last_pos = [func(self.factor_y[-1]) - self.size_x / 2, self.factor_y[-1]]

    def get_path(self):
        path = []
        for i in range(1, len(self.factor_y)):
            path.append([self.func(self.factor_y[i]) - self.func(self.factor_y[i - 1]), self.factor_y[1]])
        return path

