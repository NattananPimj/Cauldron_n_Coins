import pygame as pg

from cnc_config import Config
from cnc_herbs import *

pg.init()


class Map:
    def __init__(self):

        self.__path = []
        self.__distance = [0, 0]
        self.__bottle = [10, 0]
        self.surface = pg.Surface((Config.MAP_WIDTH, Config.MAP_HEIGHT))
        self.rect = self.surface.get_rect()
        self.__originX = Config.MAP_WIDTH / 2
        self.__originY = Config.MAP_HEIGHT / 2

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
            line.append([line[i][0]+self.__path[i][0], line[i][1]- self.__path[i][1]])
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
        factor_x = Config.FACTOR_x * 2
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
        self.__path.extend(herb.path())

    def move_along(self):
        if len(self.__path) > 0:
            path = self.__path.pop(0)
            self.__bottle[0] += path[0]
            self.__distance[0] += 1
            self.__bottle[1] += path[1]
            self.__distance[1] += 1
            print(path)


class Drawer:
    def __init__(self, m: Map, h:HerbManager):
        self.__gameinfo = None
        self.__screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.__mapsize = pg.Rect((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                                 (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 4,
                                 Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.__screen.fill(Config.COLOR['background'])
        self.__clock = pg.time.Clock()
        self.__map = m
        self.__herb = h

    def draw_brewing_screen(self):
        self.__screen.fill((Config.COLOR['background']))
        self.on_map_draw()
        self.__screen.blit(self.__map.surface,
                           ((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                            (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8,))
        self.__screen.blit(self.__herb.surface,((((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2)-150)/2
                                                , (Config.SCREEN_HEIGHT - 600)/2))

    def on_map_draw(self):
        self.__map.surface.fill((Config.COLOR['black']))
        self.__map.surface.fill((Config.COLOR['map']), self.__map.rect.inflate(-5, -5))
        # draw marks
        pg.draw.circle(self.__map.surface, (Config.COLOR['marks']), self.__map.get_position((0, 0)), 15, width=2)
        self.plot_potion()
        # draw_bottles
        pg.draw.circle(self.__map.surface, (Config.COLOR['red']), self.__map.get_bottle_pos(), 15, width=2)
        if self.__map.get_len_path() >= 2:
            pg.draw.lines(self.__map.surface, (Config.COLOR['path']), False, self.__map.get_path_line(), 1)

    def draw_herbs_block(self):
        pass


    def plot_potion(self):
        for pos in Config.POTION_POS.values():
            pg.draw.circle(self.__map.surface, (Config.COLOR['green']), self.__map.get_position(pos), 10, width=2)


    def draw_shop_screen(self):
        self.__screen.fill((Config.COLOR['background']))
