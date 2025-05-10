import pygame as pg
from cnc_config import Config
import math


class Potion:
    def __init__(self, name: str, power: int, ingredients: list):
        self.__name = name
        self.__power = power
        self.__ingredients = ingredients
        self.__price = 57
        self.__price = Config.POTION_info[self.__name]['price'] * (1 + (self.__power / 5))
        self.pic = pg.image.load('IngamePic/Potion.png')
        self.pic = pg.transform.scale(self.pic, (70, 120))
        self.symbol = pg.image.load('IngamePic/Potion_effect/'+name+'.png')
        self.symbol = pg.transform.scale(self.symbol, (40, 40))
        self.pic.blit(self.symbol, (15, 60))

    def get_name(self) -> str:
        return self.__name

    def get_power(self) -> int:
        return self.__power

    def get_price(self) -> float:
        return self.__price

    def get_cost(self) -> float:
        return sum([Config.HERB_INFO[i]['price'] for i in self.__ingredients])

    def __str__(self) -> str:
        return '{' + f"'name': '{self.__name}', 'power': {self.__power}, 'ingredients': {self.__ingredients}" + '}'

