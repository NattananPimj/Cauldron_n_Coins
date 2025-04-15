import pygame as pg

from cnc_config import Config
from cnc_herbs import *
from cnc_inventory import Inventory
from cnc_map import Map
from cnc_herbManager import HerbManager

pg.init()


class Drawer:
    def __init__(self, m: Map, h: HerbManager):
        self.__gameinfo = None
        self.__screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.__mapsize = pg.Rect((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                                 (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 4,
                                 Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.__screen.fill(Config.COLOR['background'])
        self.__clock = pg.time.Clock()
        self.__map = m
        self.__herb = h
        self.__inventory = Inventory()

        self.__uiSurface = pg.Surface((Config.UI_WIDTH, Config.UI_HEIGHT), pg.SRCALPHA)

    def get_screen(self):
        return self.__screen

    def draw_brewing_screen(self):
        self.__screen.fill((Config.COLOR['background']))
        self.on_map_draw()
        self.__screen.blit(self.__map.surface,
                           ((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                            (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8,))
        for block in self.__herb.herb_blocks:
            block.draw(self.__herb.surface)
        self.__screen.blit(self.__herb.surface,
                           ((((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2) - Config.HERB_WIDTH) / 2
                            , (Config.SCREEN_HEIGHT - Config.HERB_HEIGHT) / 2))
        self.draw_brewing_element()
        self.draw_ui()

    def draw_brewing_element(self):
        self.__screen.blit(self.__map.spatulas[self.__map.current_spatula],
                           ((Config.SCREEN_WIDTH - 250) / 2, Config.SCREEN_HEIGHT - 250 - 100))
        self.__screen.blit(self.__map.cauldron_pic, ((Config.SCREEN_WIDTH - 250) / 2, Config.SCREEN_HEIGHT - 250))

        self.__screen.blit(self.__map.waters[self.__map.current_water],
                           ((Config.SCREEN_WIDTH - 450) / 2, Config.SCREEN_HEIGHT - 250 - 120))

        self.__screen.blit(self.__map.tableR, ((Config.SCREEN_WIDTH + 250) / 2, Config.SCREEN_HEIGHT - 150))
        self.__screen.blit(self.__map.tableL, ((Config.SCREEN_WIDTH - 730) / 2, Config.SCREEN_HEIGHT - 250))
        self.__screen.blit(self.__map.bottleup, ((Config.SCREEN_WIDTH + 250) / 2, Config.SCREEN_HEIGHT - 150 - 90))

        self.__screen.blit(self.__map.cancel, ((Config.SCREEN_WIDTH + Config.MAP_WIDTH)/2 - 50,
                                 (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8 + Config.MAP_HEIGHT - 50))



    def on_map_draw(self):
        self.__map.surface.fill((Config.COLOR['black']))
        self.__map.surface.fill((Config.COLOR['map']), self.__map.rect.inflate(-5, -5))
        # draw marks
        self.__map.surface.blit(self.__map.bottleShad, self.__map.get_position((-17, 21)))
        self.plot_potion()
        # draw_bottles
        self.__map.surface.blit(self.__map.bottle_pic, self.__map.get_bottle_pos(-17, -21))
        if self.__map.get_len_path() >= 2:
            pg.draw.lines(self.__map.surface, (Config.COLOR['path']), False, self.__map.get_path_line(), 1)

    def plot_potion(self):
        for pos in Config.POTION_POS.values():
            pg.draw.circle(self.__map.surface, (Config.COLOR['green']), self.__map.get_position(pos), 10, width=2)
            self.__map.surface.blit(self.__map.bottleShad, self.__map.get_position((pos[0] - 15, pos[1] + 21)))

    def draw_shop_screen(self):
        self.__screen.fill((Config.COLOR['background']))
        self.draw_ui()

    def draw_ui(self):
        tmpR1 = pg.Rect(1, 1, Config.UI_WIDTH - 2, Config.UI_HEIGHT / 2 - 2)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['marks']), tmpR1, border_radius=100)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['map']), tmpR1.inflate(-5, -5), border_radius=100)
        self.draw_text(self.__uiSurface, f"Day {self.__inventory.get_day()}", 30, Config.UI_WIDTH / 4,
                       0, (Config.COLOR['marks']))

        tmpR2 = pg.Rect(1, Config.UI_HEIGHT / 2 + 1, Config.UI_WIDTH - 2, Config.UI_HEIGHT / 2 - 2)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['marks']), tmpR2, border_radius=100)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['map']), tmpR2.inflate(-5, -5), border_radius=100)
        self.draw_text(self.__uiSurface, f"$ {self.__inventory.get_money():.2f}", 30, Config.UI_WIDTH / 6,
                       Config.UI_HEIGHT / 2 + 1, (Config.COLOR['marks']))

        self.__screen.blit(self.__uiSurface, (Config.SCREEN_WIDTH - Config.UI_WIDTH, 0))

    @staticmethod
    def draw_text(screen, txt, size=36, x=0, y=0, color=Config.COLOR['black']):
        font = pg.font.SysFont('comicsansms', size)
        text = font.render(txt, True, color)
        screen.blit(text, (x, y))
