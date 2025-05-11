import pygame as pg

from cnc_config import Config
from cnc_inventory import Inventory
from cnc_map import Map
from cnc_herbs import Herb
import math


class HerbCabinet:
    def __init__(self, id, x, y, m):
        self.id = id
        info = Config.HERB_INFO[id]
        self.__name = info['name']
        self.__funcX = info['funcX']
        self.__funcY = info['funcY']
        self.__t = info['t']
        self.__direction = info['direction']
        self.__price = info['price']
        self.__map = m
        self.x = x
        self.y = y

        self.__image = pg.image.load('IngamePic/' + info['pic'])
        self.__image = pg.transform.scale(self.__image, (Config.HERB_WIDTH // 2 - 2, Config.HERB_HEIGHT // 8 - 2))
        self.__hitbox = self.__image.get_rect()
        self.__hitbox.topleft = (x + (((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2) - Config.HERB_WIDTH) / 2
                               , y + (Config.SCREEN_HEIGHT - Config.HERB_HEIGHT) / 2)
        self.__enable = True

    def check_click(self, mouse_pos) -> None:
        """
        if the cabinet is selected, sent herb data into map class
        :param mouse_pos: mouse position (pg.mouse.get_pos())
        :return None:
        """
        if self.__hitbox.collidepoint(mouse_pos):
            if (pg.mouse.get_pressed()[0] == 1 and self.__enable
                    and Inventory.get_instance().check_money(self.__price)):
                self.__enable = False
                # print(self.__name, 1)
                self.sent_herb()
            if pg.mouse.get_pressed()[0] == 0:
                self.__enable = True

    def check_hover(self, mouse_pos, screen) -> None:
        """
        create mini text when the mouse is hover on the cabinet to sent name and direction to user
        :param mouse_pos: mouse position (pg.mouse.get_pos())
        :param screen: screen, for drawing
        :return None:
        """
        if self.__hitbox.collidepoint(mouse_pos):
            tmps = pg.Surface((200, 25))
            tmprect = tmps.get_rect()
            pg.draw.rect(screen, pg.Color('red'), self.__hitbox, 1)
            tmps.fill((Config.COLOR['black']))
            tmps.fill((Config.COLOR['map']), tmprect.inflate(-2, -2))
            font = pg.font.SysFont('comicsansms', 15)
            text = font.render(f"{self.__name} ({self.__direction}) [${self.__price:.2f}]", True, Config.COLOR['black'])
            tmps.blit(text, (10, 0))
            screen.blit(tmps, mouse_pos)

    def sent_herb(self):
        """
        create herb object then sent to map + deduct money
        :return:
        """
        herb = Herb(self.__name, self.__funcX, self.__funcY, self.__t, self.id)
        self.__map.add_herb(herb)
        Inventory.get_instance().deduct_money(self.__price)

    def draw(self, screen):
        """
        draw the herb cabinet
        :param screen: pg.Surface
        :return:
        """
        screen.blit(self.__image, (self.x, self.y))


class HerbManager:
    """
    store herb cabinet
    """

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
