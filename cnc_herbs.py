import pygame as pg
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
