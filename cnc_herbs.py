import pygame as pg

from cnc_config import Config
import math


class Herb:

    def __init__(self, name, funcX, funcY, t: int, id:str):
        self.name = name
        # parametric equation
        self.__funcX = funcX
        self.__funcY = funcY
        self.__factor_t = [0.0001 + i / Config.MOVESPEED for i in range(Config.MOVESPEED * t)]
        self.path = self.get_path()
        self.id = id

    def get_path(self):
        path = []
        for i in range(1, len(self.__factor_t)):
            path.append(
                [
                    self.__funcX(self.__factor_t[i]) - self.__funcX(self.__factor_t[i - 1]),
                    self.__funcY(self.__factor_t[i]) - self.__funcY(self.__factor_t[i - 1]),
                ]
            )
        return path


