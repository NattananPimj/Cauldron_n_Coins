import pygame as pg

from cnc_config import Config
import math


class Herb:

    def __init__(self, name, funcX, funcY, t: int):
        self.name = name
        # parametric equation
        self.funcX = funcX
        self.funcY = funcY
        self.factor_t = [0.0001 + i/Config.MOVESPEED for i in range(Config.MOVESPEED*t)]
        self.path = self.get_path()

    def get_path(self):
        path = []
        for i in range(1, len(self.factor_t)):
            path.append(
                [
                    self.funcX(self.factor_t[i]) - self.funcX(self.factor_t[i-1]),
                    self.funcY(self.factor_t[i]) - self.funcY(self.factor_t[i-1]),
                ]
            )
        return path


