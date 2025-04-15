import time

import pygame as pg

from cnc_config import Config
from cnc_herbs import *
from cnc_potion import Potion
from cnc_inventory import Inventory


class Map:
    def __init__(self):

        self.inventory = Inventory()

        self.reset()

        self.surface = pg.Surface((Config.MAP_WIDTH, Config.MAP_HEIGHT))
        self.rect = self.surface.get_rect()
        self.__time = time.time()

        # brewing elements
        self.bottle_pic = self.add_picture('bottle.png', (36, 36))
        self.bottleShad = self.add_picture('BottleShadow.png', (36, 36))
        self.cauldron_pic = self.add_picture('Cauldron.png', (250, 250))
        self.tableR = self.add_picture('BottleTable.png', (250, 150))
        self.tableL = self.add_picture('TableL.png', (230, 250))

        self.waters = [self.add_picture("Water" + str(x) + ".png", (144, 120)) for x in range(1, 3)]
        self.water_hitbox = self.waters[0].get_rect()
        self.current_water = 0
        self.water_hitbox.topleft = ((Config.SCREEN_WIDTH - 450) / 2, Config.SCREEN_HEIGHT - 250 - 120)

        self.bottleup = self.add_picture('BottleS.png', (250, 100))
        self.bottleup_hitbox = self.bottleup.get_rect()
        self.bottleup_hitbox.topleft = ((Config.SCREEN_WIDTH + 250) / 2, Config.SCREEN_HEIGHT - 150 - 90)

        self.cancel = self.add_picture('Cancel.png', (40, 40))
        self.cancel_hitbox = self.cancel.get_rect()
        self.cancel_hitbox.topleft = ((Config.SCREEN_WIDTH + Config.MAP_WIDTH) / 2 - 50,
                               (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8 + Config.MAP_HEIGHT - 50)

        self.spatulas = [self.add_picture("Spatula" + i + ".png", (250, 166)) for i in ['L', 'M', 'R', 'M']]
        self.current_spatula = 0
        self.__animateS = True
        self.spatula_hitbox = self.spatulas[0].get_rect()
        self.spatula_hitbox.topleft = ((Config.SCREEN_WIDTH - 250) / 2, Config.SCREEN_HEIGHT - 250 - 100)

    @staticmethod
    def add_picture(filename: str, size: tuple):
        pic = pg.image.load('IngamePic/' + filename)
        pic = pg.transform.scale(pic, size)
        return pic

    def get_len_path(self):
        return len(self.__path)

    def get_distance(self):
        return [int(self.__distance[0]), int(self.__distance[1])]

    def get_position(self, coordinate: tuple[float, float], mod_x: float = 0, mod_y: float = 0):
        return (self.__originX + coordinate[0] + mod_x,
                self.__originY - coordinate[1] + mod_y)

    def get_origin(self):
        return self.__originX, self.__originY

    def get_bottle_pos(self, mod_x=0, mod_y=0):
        return self.get_position(self.__bottle, mod_x=mod_x, mod_y=mod_y)

    def get_path_line(self):
        bottle = self.get_bottle_pos()
        line = [[bottle[0], bottle[1]]]
        for i in range(len(self.__path)):
            line.append([line[i][0] + self.__path[i][0], line[i][1] - self.__path[i][1]])
        return line

    def back_to_origin(self):
        factor_x = Config.FACTOR_x
        if self.__bottle[0] == 0:
            h = 0
            k = factor_x
        else:
            slope = abs(self.__bottle[1] / self.__bottle[0])
            h = factor_x
            k = slope * factor_x

        if self.__bottle[0] >= 0:
            self.__bottle[0] -= h
        else:
            self.__bottle[0] += h

        if self.__bottle[1] >= 0:
            self.__bottle[1] -= k
        else:
            self.__bottle[1] += k

    def move_map(self, key):
        factor_x = Config.FACTOR_x * 6
        if key[pg.K_w]:
            self.__originY += factor_x
        if key[pg.K_s]:
            self.__originY -= factor_x
        if key[pg.K_a]:
            self.__originX += factor_x
        if key[pg.K_d]:
            self.__originX -= factor_x

    def add_herb(self, herb: Herb):
        # print(herb.path())
        self.__herb_used.append(herb.name)
        self.__path.extend(herb.path)

    def move_along(self):
        if len(self.__path) > 0:
            path = self.__path.pop(0)
            self.__bottle[0] += path[0]
            self.__bottle[1] += path[1]
            self.__originX -= path[0] / 3
            self.__originY += path[1] / 3

    def find_distance_btw(self, pos: tuple[float, float]):
        return ((self.__bottle[0] - pos[0]) ** 2 + (self.__bottle[1] - pos[1]) ** 2) ** 0.5

    def done_brewing(self):
        potion = None
        for p, pos in Config.POTION_POS.items():
            dis = self.find_distance_btw(pos)
            if dis <= 25:
                for tier, distance in enumerate([3, 5, 25]):
                    if dis <= distance:
                        potion = Potion(p, 3 - tier, self.__herb_used)
                        print(potion)
                        self.inventory.add_item(potion)
                        self.reset()
                        return True
        return False

    def reset(self):
        self.__path = []
        self.__distance = 0
        self.__bottle = [0, 0]
        self.__originX = Config.MAP_WIDTH / 2
        self.__originY = Config.MAP_HEIGHT / 2
        self.__herb_used = []

    def brewing(self, mouse_pos):
        if self.spatula_hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                if self.__animateS:
                    self.__animateS = False
                    self.current_spatula = (self.current_spatula + 1) % 4
                    self.__time = time.time()
                self.move_along()

        if time.time() - self.__time > 0.15:
            self.__animateS = True

    def bottlingUp(self, mouse_pos):
        if self.bottleup_hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.done_brewing()

    def cancel_brewing(self, mose_pos):
        if self.cancel_hitbox.collidepoint(mose_pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.reset()

    def add_water(self, mouse_pos):
        if self.water_hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.current_water = 1
                self.back_to_origin()

        if pg.mouse.get_pressed()[0] == 0:
            self.current_water = 0
