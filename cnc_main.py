import pygame as pg
from cnc_herbs import *
from cnc_classes import *

pg.init()

class Game:
    def __init__(self):
        self.__map = Map()
        self.__drawer = Drawer(self.__map)
        self.__state = 'map' # map / store
        self.__running = True

    def user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__running = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_a:
                    pass
                    # self.add_path()
        # hold key down
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            pass
            # self.move_to_origin()
        if key[pg.K_UP]:
            pass
            # self.move_path()

    def run(self):
        while self.__running:
            self.user_event()
            if self.__state == 'map':
                self.__drawer.draw_brewing_screen()

            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

