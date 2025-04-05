import pygame as pg
from cnc_herbs import *
from cnc_classes import *

pg.init()


class Game:
    def __init__(self):
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
                if ev.key == pg.K_p:
                    # herb = Horizontal_Herb("a", "E", lambda x: 10 * math.sin(x / 5), '', 200, 50)
                    herb = Vertical_Herb("a", "N", lambda x: 5*(10*math.log10(x/50) + 2*math.sin(x/5))-100, '',
                                         50, 200)
                    self.__map.add_herb(herb)
                if self.__state == 'shop':
                    if ev.key == pg.K_RIGHT:
                        self.__state = 'map'
        # hold key down
        key = pg.key.get_pressed()
        # self.move_to_origin()
        if key[pg.K_SPACE]:
            self.__map.move_along()
        self.__map.move_map(key)

    def run(self):
        while self.__running:
            self.user_event()
            if self.__state == 'map':
                self.__drawer.draw_brewing_screen()
            if self.__state == 'shop':
                self.__drawer.draw_shop_screen()
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
