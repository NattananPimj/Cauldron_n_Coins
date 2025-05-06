import time
from typing import List

import pygame as pg

from cnc_config import Config
from cnc_herbs import Herb
from cnc_potion import Potion
from cnc_inventory import Inventory
from dataCollecting import DataCollector


class Map:
    def __init__(self):

        self.inventory = Inventory.get_instance()
        self.dataCollector = DataCollector()

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
        self.compass = self.add_picture("compass.png", (120, 120))
        self.question = self.add_picture("questionmark.png", (70, 70))
        self.question_hitbox = self.question.get_rect()
        self.question_hitbox.topleft = (((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2) + Config.MAP_WIDTH - 70,
                                        (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8)

        self.manual = self.add_picture("manual.png", (800, 600))

        self.potion_symbol = {}
        for name, pos in Config.POTION_POS.items():
            tmp = self.add_picture('/Potion_effect/' + name + '.png', (20, 20))
            self.potion_symbol[name] = tmp

    def reset(self):
        """
        reset to origin and delete all path
        :return:
        """

        self.__path = []
        self.__distance = 0
        self.__bottle = [0, 0]
        self.__originX = Config.MAP_WIDTH / 2
        self.__originY = Config.MAP_HEIGHT / 2
        self.__herb_used = []
        self.__traveled = 0

    def get_herb_used_data(self):
        return self.__herb_used

    @staticmethod
    def add_picture(filename: str, size: tuple):
        pic = pg.image.load('IngamePic/' + filename)
        pic = pg.transform.scale(pic, size)
        return pic

    def get_len_path(self):
        return len(self.__path)

    def get_distance(self):
        return [int(self.__distance[0]), int(self.__distance[1])]

    def get_origin(self):
        return self.__originX, self.__originY

    def get_traveled(self):
        return self.__traveled

    def get_position(self, coordinate: tuple[float, float], mod_x: float = 0, mod_y: float = 0) -> tuple[float, float]:
        """

        :param coordinate: the coordinate on map (0, 0) as origin
        :param mod_x: modifying x, positive to the right
        :param mod_y: modifying y, positive to the bottom
        :return tuple[float, float]: getting real position for drawing
        """
        return (self.__originX + coordinate[0] + mod_x,
                self.__originY - coordinate[1] + mod_y)

    def get_bottle_pos(self, mod_x=0, mod_y=0):
        """
        for adding stuff that come and stick with bottle
        :param mod_x: modifying x, positive to the right
        :param mod_y: modifying y, positive to the bottom
        :return tuple[float, float]: getting real position for drawing
        """
        return self.get_position(self.__bottle, mod_x=mod_x, mod_y=mod_y)

    def get_path_line(self) -> List[tuple[float, float]]:
        """
        getting path line, for drawing path
        :return list:
        """
        bottle = self.get_bottle_pos()
        line = [[bottle[0], bottle[1]]]
        for i in range(len(self.__path)):
            line.append([line[i][0] + self.__path[i][0], line[i][1] - self.__path[i][1]])
        return line

    def get_slope(self, factor_x=Config.FACTOR_x):
        if self.__bottle[0] == 0:
            h = 0
            k = factor_x
        else:
            slope = abs(self.__bottle[1] / self.__bottle[0])
            h = factor_x
            k = slope * factor_x

        if self.__bottle[0] >= 0:
            h *= -1

        if self.__bottle[1] >= 0:
            k *= -1

        return h, k

    def back_to_origin(self) -> None:
        """
        moving bottle towards origin no matter where the bottle at
        :return:
        """
        h, k = self.get_slope()
        self.__bottle[0] += h
        self.__bottle[1] += k

    def move_map(self, key) -> None:
        """
        moving map to look around
        :param key: W A S D for up, left, down and, right respectively
        :return:
        """
        factor_x = Config.FACTOR_x * 20
        if key[pg.K_w] and self.__originY <= ((Config.MAP_HEIGHT / 2) + 900):
            self.__originY += factor_x
        if key[pg.K_s] and self.__originY >= ((Config.MAP_HEIGHT / 2) - 900):
            self.__originY -= factor_x
        if key[pg.K_d] and self.__originX >= ((Config.MAP_WIDTH / 2) - 900):
            self.__originX -= factor_x
        if key[pg.K_a] and self.__originX <= ((Config.MAP_WIDTH / 2) + 900):
            self.__originX += factor_x

    def add_herb(self, herb: Herb):
        """
        adding herb for path and collecting data
        :param herb:
        :return:
        """
        self.__herb_used.append(herb.id)
        self.__path.extend(herb.path)

    def move_along(self):
        """
        Move along the created path
        :return:
        """
        if len(self.__path) > 0:
            path = self.__path.pop(0)
            self.__bottle[0] += path[0]
            self.__bottle[1] += path[1]
            self.__originX -= path[0] / 3
            self.__originY += path[1] / 3

            self.__traveled += ((path[0]) ** 2 + (path[0]) ** 2) ** 0.5
            # print(self.__traveled, path,':', self.__bottle,self.find_distance_btw((0,0)))

    def find_distance_btw(self, pos: tuple[float, float]):
        return ((self.__bottle[0] - pos[0]) ** 2 + (self.__bottle[1] - pos[1]) ** 2) ** 0.5

    def done_brewing(self) -> bool:
        """
        checking the position of bottle and bottle shadow.
        if successful, create potion and sent directly to Inventory.
        then reset.
        :return bool:
        """
        potion = None
        for p, pos in Config.POTION_POS.items():
            dis = self.find_distance_btw(pos)
            if dis <= 25:
                for tier, distance in enumerate([3, 5, 25]):
                    if dis <= distance:
                        potion = Potion(p, 3 - tier, self.__herb_used)
                        print(potion)
                        self.inventory.add_item(potion)
                        # add data
                        self.dataCollector.add_data_herb(self.__herb_used)
                        self.dataCollector.add_distance_data(p, 3 - tier, self.__traveled)
                        self.reset()
                        return True
        return False

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
        self.__check_click(mouse_pos, self.bottleup_hitbox, self.done_brewing)

    def cancel_brewing(self, mose_pos):
        self.__check_click(mose_pos, self.cancel_hitbox, self.reset)

    def add_water(self, mouse_pos):
        self.__check_click(mouse_pos, self.water_hitbox, self.back_to_origin,
                           lambda: self.change_current_water(1),
                           lambda: self.change_current_water(0))

    def change_current_water(self, to: int):
        self.current_water = to

    def open_manual(self, mouse):
        if self.question_hitbox.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1:
                return True
        return False

    @staticmethod
    def __check_click(mouse_pos, hitbox: pg.Rect, func1_1, func1_2=None, func2=None) -> None:
        """
        checking if mouse is click on the hit box and do the function
        :param mouse_pos: mouse position (pg.mouse.get_pos())
        :param hitbox: Rect with topleft filled
        :param func1_1: function that executed when the mouse is clicked
        :param func1_2: function that executed when the mouse is clicked(optional)
        :param func2: function that executed when the mouse is not clicked(optional),
                      mostly for return to original position
        :return:
        """
        if hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                func1_1()
                if func1_2 is not None:
                    func1_2()
        if pg.mouse.get_pressed()[0] == 0:
            if func2 is not None:
                func2()
