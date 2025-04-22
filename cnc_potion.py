import pygame as pg
from cnc_config import Config
import math


class Potion:
    def __init__(self, name: str, power: int, ingredients: list):
        self.__name = name
        self.__power = power
        self.__ingredients = ingredients
        self.__price = Config.POTION_info[self.__name]['price'] * (1 + (self.__power / 3))
        self.pic = pg.image.load('IngamePic/Potion.png')
        self.pic = pg.transform.scale(self.pic, (70, 120))
        # TODO: making logo/ symbol for each potion and add it to dict

    def get_name(self):
        return self.__name

    def get_power(self):
        return self.__power

    def get_price(self):
        return self.__price

    def check_ingredients(self, ingredient):
        return ingredient in self.__ingredients

    def __str__(self):
        return '{' + f"'name': '{self.__name}', 'power': {self.__power}, 'ingredients': {self.__ingredients}" + '}'

