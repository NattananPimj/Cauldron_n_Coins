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
        self.title = pg.image.load('IngamePic/Title.jpg')
        self.play_button = pg.Rect((Config.SCREEN_WIDTH - 400) / 2, (Config.SCREEN_HEIGHT * (2 / 3)), 400, 100)
        self.stat_icon = pg.image.load('IngamePic/Stat_icon.png')
        self.stat_icon = pg.transform.scale(self.stat_icon, (100, 100))
        self.stat_rect = self.stat_icon.get_rect()
        self.stat_rect.topleft = Config.SCREEN_WIDTH - 110, Config.SCREEN_HEIGHT - 110
        self.pop_up_rect = pg.Rect((Config.SCREEN_WIDTH - 500)/2, (Config.SCREEN_HEIGHT - 300)/2,
                                   500, 300)

        self.__tutorial = [pg.image.load('IngamePic/Tutorials/tutorial'+str(i)+'.png') for i in range(1, 6)]
        self.__tutorial_page = 0

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
        # draw obs
        for obs in self.__map.obstacles:
            obs.draw_obs(self.__map.surface, self.__map.get_position(obs.get_position()))

        # draw marks
        self.__map.surface.blit(self.__map.bottleShad, self.__map.get_position((-17, 21)))
        self.plot_potion()

        if self.__map.get_len_path() >= 2:
            pg.draw.lines(self.__map.surface, (Config.COLOR['path']), False, self.__map.get_path_line(), 2)
        h, k = self.__map.get_slope(1)
        l = (h ** 2 + k ** 2) ** 0.5
        pg.draw.line(self.__map.surface, (Config.COLOR['inventory_bg']), self.__map.get_bottle_pos(),
                     self.__map.get_bottle_pos((h / l) * 40, (-k / l) * 40))

        # draw_bottles
        # pg.draw.circle(self.__map.surface, (Config.COLOR['red']), self.__map.get_bottle_pos(),15)
        self.__map.surface.blit(self.__map.bottle_pic, self.__map.get_bottle_pos(-17 + self.__map.shaking[0],
                                                                                 -21+ self.__map.shaking[0]))
        self.__map.surface.blit(self.__map.compass, (0, 0))
        self.__map.surface.blit(self.__map.question, (Config.MAP_WIDTH - 70, 0))

        pg.draw.rect(self.__map.surface, Config.COLOR['black'], self.__map.rect, width=3)

    def draw_manual(self):
        self.__screen.blit(self.__map.manual, ((Config.SCREEN_WIDTH - 800) / 2, (Config.SCREEN_HEIGHT - 600) / 2))

    def plot_potion(self):
        for name, pos in Config.POTION_POS.items():
            self.__map.surface.blit(self.__map.bottleShad, self.__map.get_position((pos[0] - 15, pos[1] + 21)))
            self.__map.potion_symbol[name].convert_alpha(self.__map.surface)
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
            if self.__customerM.current_customer.reaction is not None:
                self.__screen.blit(
                    self.__customerM.current_customer.reaction_pic[self.__customerM.current_customer.reaction],
                    (self.__customerM.current_customer.x, 200))
            # draw dialog
            for i, lines in enumerate(self.__customerM.current_customer.dialog):
                self.draw_text(dialogBox,
                               lines, 30, 25, 25 + (i * 40), Config.COLOR['marks'])
            self.__screen.blit(dialogBox, (300, 40))
            # draw buttons
            for key, value in self.__customerM.buttons.items():
                pg.draw.rect(self.__screen, Config.COLOR['marks'], value[0], border_radius=20)
                pg.draw.rect(self.__screen, Config.COLOR['map'], value[0].inflate(-5, -5), border_radius=20)
                self.draw_text(self.__screen, key, 30,
                               value[0].x + (30), value[0].y + 5, Config.COLOR['marks'])

        self.__customerM.draw_offering(self.__screen)
        cashier = self.__customerM.cashier.copy()
        if self.__customerM.offered is not None:
            self.draw_text(cashier, f"{self.__customerM.get_price():.2f}", 30, 70, 20, Config.COLOR['marks'])
        self.__screen.blit(cashier, (500, 400))
        # table
        pg.draw.rect(self.__screen, Config.COLOR['brown'],
                     (0, 400 + 228, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT - 600))
        self.draw_inventory()
        self.draw_ui()

    def draw_haggle(self):
        self.__screen.blit(self.__customerM.haggle.surface, (400, 100))
        self.__customerM.haggle.surface.fill(Config.COLOR['marks'])
        self.__customerM.haggle.surface.fill(Config.COLOR['haggle1'], self.__customerM.haggle.surfaceR.inflate(-5, -5))
        pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['haggle2'], pg.Rect(10, 150, 480, 50))
        self.__customerM.haggle.surface.blit(self.__customerM.haggle.details, (500 - 227, 2))

        for dif, r in self.__customerM.haggle.difficulty_button.items():
            color = Config.COLOR['haggle2'] if dif == self.__customerM.haggle.get_level() else Config.COLOR['haggle1']
            pg.draw.rect(self.__customerM.haggle.surface, color, r)
            # pg.draw.rect(self.__screen,Config.COLOR['red'], self.__customerM.haggle.difficulty_hitbox[1])
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['marks'], r, width=1)

        txt_surface = self.__customerM.haggle.surface.copy()

        for i, txt in enumerate(['I', 'II', 'III']):
            self.draw_text(txt_surface, txt, 40, 30 + (91 * i) - (8 * i), 40, Config.COLOR['marks'])
        self.draw_text(txt_surface,
                       f"+{self.__customerM.offered.get_price() * 0.5:.2f}", 20, 500 - 190, 50, Config.COLOR['marks'])
        self.draw_text(txt_surface,
                       f"-{self.__customerM.offered.get_price() * 0.5:.2f}", 20, 500 - 80, 50, Config.COLOR['marks'])
        self.draw_text(txt_surface, "Press Space to Haggle", 36, 50, 220, Config.COLOR['marks'])

        self.__customerM.haggle.surface.blit(txt_surface, (0, 0))

        for box in self.__customerM.haggle.done_rect:
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['black'], box)
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['green'], box.inflate(-2, -2))
        for bar in self.__customerM.haggle.hagglebar:
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['black'], bar)
            pg.draw.rect(self.__customerM.haggle.surface, Config.COLOR['hagglebar'], bar.inflate(-2, -2))
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

    def draw_title(self):

        pg.draw.rect(self.title, Config.COLOR['marks'], self.play_button, border_radius=50)
        pg.draw.rect(self.title, Config.COLOR['haggle1'], self.play_button.inflate(-3, -3), border_radius=50)
        self.draw_text(self.title, 'Play', 56, (Config.SCREEN_WIDTH - 400 + 275) / 2,
                       (Config.SCREEN_HEIGHT * (2 / 3)), Config.COLOR['marks'])
        self.draw_text(self.title, f"Username: {self.__inventory.get_name()}",
                       y=Config.SCREEN_HEIGHT - 50, color=Config.COLOR['marks'])

        pg.draw.rect(self.title, Config.COLOR['marks'], self.stat_rect, border_radius=20)
        pg.draw.rect(self.title, Config.COLOR['map'], self.stat_rect.inflate(-5, -5), border_radius=20)
        self.title.blit(self.stat_icon, (Config.SCREEN_WIDTH - 110, Config.SCREEN_HEIGHT - 110))
        self.__screen.blit(self.title, (0, 0))

    def pop_up(self):
        pg.draw.rect(self.__screen, Config.COLOR['marks'], self.pop_up_rect)
        pg.draw.rect(self.__screen, Config.COLOR['map'], self.pop_up_rect.inflate(-5, -5))
        self.draw_text(self.__screen, "Look like you use all your money?",
                       20, (Config.SCREEN_WIDTH - 500)/2 + 100, (Config.SCREEN_HEIGHT - 300)/2 + 50)
        self.draw_text(self.__screen, "You already went bankrupt",
                       20, (Config.SCREEN_WIDTH - 500) / 2 + 120, (Config.SCREEN_HEIGHT - 300) / 2 + 100)
        self.draw_text(self.__screen, "Press Space to restart",
                       20, (Config.SCREEN_WIDTH - 500) / 2 + 140, (Config.SCREEN_HEIGHT - 300) / 2 + 180)


    def play(self, mouse):
        if self.play_button.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1:
                return True
        return False

    def open_stat(self, mouse):
        if self.stat_rect.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1:
                return True
        return False

    def draw_tutorial(self):
        self.__screen.blit(self.__tutorial[self.__tutorial_page],
                           ((Config.SCREEN_WIDTH - 800) / 2, (Config.SCREEN_HEIGHT - 600) / 2))

    def next_page(self):
        if self.__tutorial_page == 4:
            return False
        self.__tutorial_page += 1
        return True

    def prev_page(self):
        if self.__tutorial_page > 0:
            self.__tutorial_page -= 1

    def set_zero(self):
        self.__tutorial_page = 0



