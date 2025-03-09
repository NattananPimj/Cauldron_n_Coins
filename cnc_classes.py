import pygame as pg
from cnc_config import Config


class Map:
    pass

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

    def get_path(self, distance):
        path = []
        if distance < len(self.factor_x):
            for i in range(distance, len(self.factor_x)):
                path.append([self.size/10, self.func(self.factor_x[i]) - self.factor_x[i-1]])
        return path
    
    def get_cood(self, distance):
        line = []
        if distance < len(self.factor_x):
            for i in range(distance, len(self.factor_x)):
                line.append([self.factor_x[i], self.func(self.factor_x[i]) + self.size_y/2])
        return line

    
class E_Herb:
    def __init__(self, name, func, file, x, y):
        super().__init__(name, "E", func, file, x, y)
        self.factor_x = [i/10 for i in range(x*10)]

    
    

        