import pygame as pg

from cnc_config import Config
from cnc_map import Map
from cnc_herbs import Herb
import math


class HerbCabinet:
    def __init__(self, id, x, y, m):
        info = Config.HERB_INFO[id]
        self.name = info['name']
        self.funcX = info['funcX']
        self.funcY = info['funcY']
        self.t = info['t']
        self.direction = info['direction']
        self.__map = m

        self.image = pg.image.load('IngamePic/' + info['pic'])
        self.image = pg.transform.scale(self.image, (Config.HERB_WIDTH // 2 - 2, Config.HERB_HEIGHT // 8 - 2))
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (x, y)
        self.enable = True

    def check_click(self, mouse_pos):
        if self.hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.enable:
                self.enable = False
                print(self.name, 1)
                self.sent_herb()
            if pg.mouse.get_pressed()[0] == 0:
                self.enable = True

    def sent_herb(self):
        herb = Herb(self.name, self.funcX, self.funcY, self.t)
        self.__map.add_herb(herb)

    def draw(self, screen):
        screen.blit(self.image, (self.hitbox.x, self.hitbox.y))


class HerbManager:
    # 16 herb
    __HERB_INFO = Config.HERB_INFO

    def __init__(self, m: Map):
        self.surface = pg.Surface((Config.HERB_WIDTH, Config.HERB_HEIGHT))
        self.__map = m
        self.herb_blocks = []
        self.add_herb_block()

    def add_herb_block(self):
        ids = list(Config.HERB_INFO.keys())
        i = 0
        for y in range(1, Config.HERB_HEIGHT + 1, Config.HERB_HEIGHT // 8):
            for x in range(1, Config.HERB_WIDTH + 1, Config.HERB_WIDTH // 2):
                tmpR = HerbCabinet(ids[i], x, y, self.__map)
                i += 1
                self.herb_blocks.append(tmpR)

