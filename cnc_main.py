import pygame as pg
from cnc_herbs import *
from cnc_classes import *
from cnc_config import Config
from cnc_inventory import Inventory
from cnc_map import Map
from cnc_herbManager import HerbManager

pg.init()


class Game:
    """
    main class for the game, run everything here
    """
    def __init__(self, name: str = 'lilly'):
        """
        :param name: username for register the save. if not sign in yet, create new one

        import all the class in
        """
        self.__inventory = Inventory(name)
        self.__map = Map()
        self.__herbs = HerbManager(self.__map)
        self.__drawer = Drawer(self.__map, self.__herbs)
        self.__state = 'map'  # map / store

        self.__running = True

    def user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__running = False
            if ev.type == pg.KEYDOWN:

                if self.__state == 'map':
                    if ev.key == pg.K_LEFT:
                        self.__state = 'shop'

                if self.__state == 'shop':
                    if ev.key == pg.K_RIGHT:
                        self.__state = 'map'
        # hold key down
        key = pg.key.get_pressed()
        # self.move_to_origin()
        if key[pg.K_SPACE]:
            self.__map.back_to_origin()
        self.__map.move_map(key)

    def run(self):
        while self.__running:
            """
            user event + checking mouse clicking
            """
            mouse = pg.mouse.get_pos()
            self.user_event()

            if self.__state == 'map':
                self.__drawer.draw_brewing_screen()
                for block in self.__herbs.herb_blocks:
                    block.check_hover(mouse, self.__drawer.get_screen())
                    block.check_click(mouse)
                self.__map.brewing(mouse)
                self.__map.bottlingUp(mouse)
                self.__map.cancel_brewing(mouse)
                self.__map.add_water(mouse)

            if self.__state == 'shop':
                self.__drawer.draw_shop_screen()
            pg.display.update()


if __name__ == "__main__":
    # name = input('Put ur name to lock in: ')
    name = 'lilly'
    game = Game(name)
    game.run()
