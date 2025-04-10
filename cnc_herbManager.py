import pygame as pg

from cnc_config import Config
from cnc_map import Map
from cnc_herbs import *
import math


class HerbManager:
    # 16 herb
    __HERB_INFO = Config.HERB_INFO

    def __init__(self, m: Map):
        self.surface = pg.Surface((Config.HERB_WIDTH, Config.HERB_HEIGHT))
        self.__map = m
        self.herb_blocks = []
        self.add_herb_block()

    def add_herb_block(self):
        for i in range(1, Config.HERB_HEIGHT + 2, Config.HERB_HEIGHT // 8):
            for j in range(1, Config.HERB_WIDTH + 2, Config.HERB_WIDTH // 2):
                tmpR = pg.Rect(j, i, Config.HERB_WIDTH // 2 - 2, Config.HERB_HEIGHT // 8 - 2)  # 98, 78
                self.herb_blocks.append(tmpR)

    def add_herb(self, herb_name):
        info = self.__HERB_INFO[herb_name]
        herb = Herb(
            info['name'],
            info['funcX'],
            info['funcY'],
            info['t']
        )
        self.__map.add_herb(herb)
