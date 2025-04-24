import pygame as pg

from cnc_config import Config
from cnc_herbs import *
from cnc_inventory import Inventory, CustomerManager, Customer
from cnc_map import Map
from cnc_herbManager import HerbManager

pg.init()


class Drawer:
    """
    most drawing here
    """

    def __init__(self, m: Map, h: HerbManager, c: CustomerManager):
        self.__gameinfo = None
        self.__screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.__mapsize = pg.Rect((Config.SCREEN_WIDTH - Config.MAP_WIDTH) / 2,
                                 (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 4,
                                 Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.__screen.fill(Config.COLOR['background'])
        self.__clock = pg.time.Clock()
        self.__map = m
        self.__herb = h
        self.__customerM = c
        self.__inventory = Inventory.get_instance()

        self.__uiSurface = pg.Surface((Config.UI_WIDTH, Config.UI_HEIGHT), pg.SRCALPHA)
        self.bedroom = pg.image.load('IngamePic/Bedroom.jpg')
        self.bed = pg.Rect(20, 1 * Config.SCREEN_HEIGHT / 2, Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT / 3)
        self.bed_enable = True

    def check_sleep(self, mouse):
        if self.bed.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.bed_enable:
                self.bed_enable = False
                return True
            if pg.mouse.get_pressed()[0] == 0:
                self.bed_enable = True
        return False


    def get_screen(self):
        return self.__screen

    def draw_brewing_screen(self) -> None:
        """
        for everything happen on brewing screen
        """
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
        self.draw_inventory()
        self.draw_ui()

    def draw_brewing_element(self) -> None:
        """
        all brewing elements.
        Cauldron, shelf, bottle, water
        :return None:
        """
        self.__screen.blit(self.__map.spatulas[self.__map.current_spatula],
                           ((Config.SCREEN_WIDTH - 250) / 2, Config.SCREEN_HEIGHT - 250 - 100))
        self.__screen.blit(self.__map.cauldron_pic, ((Config.SCREEN_WIDTH - 250) / 2, Config.SCREEN_HEIGHT - 250))

        self.__screen.blit(self.__map.waters[self.__map.current_water],
                           ((Config.SCREEN_WIDTH - 450) / 2, Config.SCREEN_HEIGHT - 250 - 120))
        # print(self.__map.current_water)

        self.__screen.blit(self.__map.tableR, ((Config.SCREEN_WIDTH + 250) / 2, Config.SCREEN_HEIGHT - 150))
        self.__screen.blit(self.__map.tableL, ((Config.SCREEN_WIDTH - 730) / 2, Config.SCREEN_HEIGHT - 250))
        self.__screen.blit(self.__map.bottleup, ((Config.SCREEN_WIDTH + 250) / 2, Config.SCREEN_HEIGHT - 150 - 90))

        self.__screen.blit(self.__map.cancel, ((Config.SCREEN_WIDTH + Config.MAP_WIDTH) / 2 - 50,
                                               (Config.SCREEN_HEIGHT - Config.MAP_HEIGHT) / 8 + Config.MAP_HEIGHT - 50))

    def on_map_draw(self) -> None:
        """
        everything happen on map surface
        """
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
        for name, pos in Config.POTION_POS.items():
            self.__map.surface.blit(self.__map.bottleShad, self.__map.get_position((pos[0] - 15, pos[1] + 21)))
            self.__map.surface.blit(self.__map.potion_symbol[name], self.__map.get_position((pos[0] - 7, pos[1] + 10)))


    def draw_shop_screen(self):
        """
            for everything happen on shop screen
        """
        self.__screen.fill((Config.COLOR['background']))
        dialogBox = self.__customerM.dialogBox.copy()
        if self.__customerM.prev_customer is not None:
            self.__screen.blit(self.__customerM.prev_customer.pic,
                               (self.__customerM.prev_customer.x, 200))

        if self.__customerM.current_customer is not None:
            self.__screen.blit(self.__customerM.current_customer.pic,
                               (self.__customerM.current_customer.x, 200))
            # draw dialog
            for i, lines in enumerate(self.__customerM.current_customer.dialog):
                self.draw_text(dialogBox,
                               lines, 30, 25, 25 + (i * 40), Config.COLOR['marks'])
            self.__screen.blit(dialogBox, (300, 40))
            for key, value in self.__customerM.buttons.items():
                pg.draw.rect(self.__screen, Config.COLOR['marks'], value[0], border_radius=20)
                pg.draw.rect(self.__screen, Config.COLOR['map'], value[0].inflate(-5, -5), border_radius=20)
                self.draw_text(self.__screen, key, 30,
                               value[0].x + (30), value[0].y + 5, Config.COLOR['marks'])



        self.__customerM.draw_offering(self.__screen)


        self.draw_inventory()
        self.draw_ui()

    def draw_haggle(self):
        self.__screen.blit(self.__customerM.haggle.surface, (400, 100))
        self.__customerM.haggle.surface.fill(Config.COLOR['marks'])
        for bar in self.__customerM.haggle.hagglebar:
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['red'], bar)
        self.__customerM.haggle.draw_triangle()

    def draw_ui(self):
        """
        draw ui
        :return None:
        """
        dayRect = pg.Rect(1, 1, Config.UI_WIDTH - 2, Config.UI_HEIGHT / 2 - 2)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['marks']), dayRect, border_radius=100)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['map']), dayRect.inflate(-5, -5), border_radius=100)
        self.draw_text(self.__uiSurface, f"Day {self.__inventory.get_day()}", 30, Config.UI_WIDTH / 4,
                       0, (Config.COLOR['marks']))

        moneyRect = pg.Rect(1, Config.UI_HEIGHT / 2 + 1, Config.UI_WIDTH - 2, Config.UI_HEIGHT / 2 - 2)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['marks']), moneyRect, border_radius=100)
        pg.draw.rect(self.__uiSurface, (Config.COLOR['map']), moneyRect.inflate(-5, -5), border_radius=100)
        self.draw_text(self.__uiSurface, f"$ {self.__inventory.get_money():.2f}", 30, Config.UI_WIDTH / 6,
                       Config.UI_HEIGHT / 2 + 1, (Config.COLOR['marks']))

        self.__screen.blit(self.__uiSurface, (Config.SCREEN_WIDTH - Config.UI_WIDTH, 0))

    def draw_inventory(self):
        self.__screen.blit(self.__inventory.surface, (Config.SCREEN_WIDTH - Config.INV_WIDTH, Config.UI_HEIGHT))
        self.__inventory.surface.fill((Config.COLOR['inventory_bg']))
        for slot in self.__inventory.get_slots():
            slot.draw(self.__inventory.surface)
        # draw arrow up
        pg.draw.polygon(self.__screen, Config.COLOR['marks'],
                        ((Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT / 2),
                         (Config.SCREEN_WIDTH - Config.INV_WIDTH, Config.SCREEN_HEIGHT / 2),
                         (Config.SCREEN_WIDTH - Config.INV_WIDTH - 20, Config.SCREEN_HEIGHT / 2 - 50)), width=3)
        # draw arrow up
        pg.draw.polygon(self.__screen, Config.COLOR['marks'],
                        ((Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT / 2 + 10),
                         (Config.SCREEN_WIDTH - Config.INV_WIDTH, Config.SCREEN_HEIGHT / 2 + 10),
                         (Config.SCREEN_WIDTH - Config.INV_WIDTH - 20, Config.SCREEN_HEIGHT / 2 + 60)), width=3)

    @staticmethod
    def draw_text(screen, txt, size=36, x=0, y=0, color=Config.COLOR['black']):
        font = pg.font.SysFont('comicsansms', size)
        text = font.render(txt, True, color)
        screen.blit(text, (x, y))

    def draw_bedroom(self):
        self.__screen.fill((Config.COLOR['background']))
        self.__screen.blit(self.bedroom, (0, 0))
        # pg.draw.rect(self.__screen, Config.COLOR['red'], self.bed)

        self.draw_ui()
