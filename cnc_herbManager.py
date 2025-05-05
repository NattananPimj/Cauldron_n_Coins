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
        self.name = info['name']
        self.funcX = info['funcX']
        self.funcY = info['funcY']
        self.t = info['t']
        self.direction = info['direction']
        self.price = info['price']
        self.__map = m
        self.x = x
        self.y = y

        self.image = pg.image.load('IngamePic/' + info['pic'])
        self.image = pg.transform.scale(self.image, (Config.HERB_WIDTH // 2 - 2, Config.HERB_HEIGHT // 8 - 2))
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (x + (((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2) - Config.HERB_WIDTH) / 2
                               , y +(Config.SCREEN_HEIGHT - Config.HERB_HEIGHT) / 2)
        self.enable = True

    def check_click(self, mouse_pos) -> None:
        """
        if the cabinet is selected, sent herb data into map class
        :param mouse_pos: mouse position (pg.mouse.get_pos())
        :return None:
        """
        if self.hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.enable:
                self.enable = False
                print(self.name, 1)
                self.sent_herb()
            if pg.mouse.get_pressed()[0] == 0:
                self.enable = True

    def check_hover(self, mouse_pos, screen) -> None:
        """
        create mini text when the mouse is hover on the cabinet to sent name and direction to user
        :param mouse_pos: mouse position (pg.mouse.get_pos())
        :param screen: screen, for drawing
        :return None:
        """
        if self.hitbox.collidepoint(mouse_pos):
            tmps = pg.Surface((200, 25))
            tmprect = tmps.get_rect()
            pg.draw.rect(screen, pg.Color('red'), self.hitbox, 1)
            tmps.fill((Config.COLOR['black']))
            tmps.fill((Config.COLOR['map']), tmprect.inflate(-2, -2))
            font = pg.font.SysFont('comicsansms', 15)
            text = font.render(f"{self.name} ({self.direction}) [${self.price:.2f}]", True, Config.COLOR['black'])
            tmps.blit(text, (10, 0))
            screen.blit(tmps, mouse_pos)

    def sent_herb(self):
        """
        create herb object then sent to map + deduct money
        :return:
        """
        herb = Herb(self.name, self.funcX, self.funcY, self.t, self.id)
        self.__map.add_herb(herb)
        Inventory.get_instance().deduct_money(self.price)

    def draw(self, screen):
        """
        draw the herb cabinet
        :param screen: pg.Surface
        :return:
        """
        screen.blit(self.image, (self.x, self.y))


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
