import pygame as pg
from pygame import mixer
import tkinter as tk
from cnc_draw import Drawer
from cnc_config import Config
from cnc_inventory import Inventory, CustomerManager
from cnc_map import Map
from cnc_herbManager import HerbManager
from datadispley import DataApp

pg.init()


class Game:
    """
    main class for the game, run everything here
    """

    def __init__(self, name: str):
        """
        :param name: username for register the save. if not sign in yet, create new one

        import all the class in
        """
        pg.display.set_caption('Cauldron and Coins')
        pg.display.set_icon(pg.image.load('IngamePic/Cauldron.png'))

        self.__inventory = Inventory(name)
        self.__customer_manager = CustomerManager()
        self.__inventory.add_manager(self.__customer_manager)
        self.__map = Map()
        self.__herbs = HerbManager(self.__map)
        self.__drawer = Drawer(self.__map, self.__herbs, self.__customer_manager)
        self.__state = 'title'  # title
        self.__prev_state = 'map'
        self.__music_file = 'Music/misty-wind-troubadour-164146.ogg'

        self.__running = True

    def __user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.__running = False

            if ev.type == pg.MOUSEWHEEL:
                self.__inventory.move_up_down(ev.y)
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    if self.__state == 'title':
                        self.__running = False
                    self.__prev_state = self.__state
                    self.__state = 'title'

                if self.__state == 'tutorial':
                    if ev.key == pg.K_SPACE or ev.key == pg.K_RIGHT:
                        if not self.__drawer.next_page():
                            self.__state = self.__prev_state
                    if ev.key == pg.K_LEFT:
                        self.__drawer.prev_page()
                    if ev.key == pg.K_ESCAPE:
                        self.__state = self.__prev_state

                if self.__state == 'map':
                    if ev.key == pg.K_LEFT:
                        self.__state = 'shop'
                    if ev.key == pg.K_UP:
                        self.__state = 'bedroom'
                        self.__prev_state = 'map'
                    if ev.key == pg.K_t:
                        self.__drawer.set_zero()
                        self.__state = 'tutorial'
                        self.__prev_state = 'map'

                if self.__state == 'manual':
                    if ev.key == pg.K_SPACE:
                        self.__state = 'map'

                if self.__state == 'shop':
                    if ev.key == pg.K_RIGHT:
                        self.__state = 'map'
                    if ev.key == pg.K_UP:
                        self.__state = 'bedroom'
                        self.__prev_state = 'shop'
                    if ev.key == pg.K_t:
                        self.__drawer.set_zero()
                        self.__state = 'tutorial'
                        self.__prev_state = 'shop'

                if self.__state == 'haggle':
                    if ev.key == pg.K_SPACE:
                        # temporary
                        self.__customer_manager.haggle.start = True
                        self.__customer_manager.haggle.haggle_action()
                        self.__customer_manager.haggle.click_done()
                        # print(self.__customer_manager.haggle.multiplier)

                if self.__state == 'bedroom':
                    if ev.key == pg.K_DOWN:
                        if self.__prev_state == 'bedroom':
                            self.__prev_state = 'map'
                        self.__state = self.__prev_state
                    if ev.key == pg.K_t:
                        self.__drawer.set_zero()
                        self.__state = 'tutorial'
                        self.__prev_state = 'bedroom'

                if self.__state == 'restart':
                    if ev.key == pg.K_SPACE:
                        self.__inventory.restart()
                        self.__inventory.save_data()
                        self.__state = 'title'

        # hold key down
        key = pg.key.get_pressed()
        # self.move_to_origin()
        if key[pg.K_SPACE]:
            self.__map.back_to_origin()
        self.__map.move_map(key)

    def run(self):
        self.__music()
        while self.__running:
            """
            user event + checking mouse clicking
            """
            mouse = pg.mouse.get_pos()
            self.__user_event()
            self.__inventory.check_arrow(mouse)

            if self.__state == 'map':
                self.__run_map(mouse)

            if self.__state == 'restart':
                self.__drawer.draw_brewing_screen()
                self.__drawer.pop_up()

            if self.__state == 'manual':
                self.__drawer.draw_brewing_screen()
                self.__drawer.draw_manual()

            if self.__state == 'shop':
                self.__run_shop(mouse)

            if self.__state == 'bedroom':
                self.__drawer.draw_bedroom()
                if self.__drawer.check_sleep(mouse):
                    self.__reset()

            if self.__state == 'haggle':
                self.__run_haggle(mouse)

            if self.__state == 'title':
                self.__run_title(mouse)

            if self.__state == 'tutorial':
                self.__run_tutorial()

            pg.display.update()

    def __music(self):
        mixer.init()
        mixer.music.load(self.__music_file)
        mixer.music.play(-1)
        mixer.music.set_volume(Config.MUSIC_VOLUME)

    def __run_map(self, mouse):
        self.__check_tutorial()
        self.__drawer.draw_brewing_screen()
        for block in self.__herbs.__herb_blocks:
            block.check_hover(mouse, self.__drawer.get_screen())
            block.check_click(mouse)
        self.__map.brewing(mouse)
        self.__map.bottlingUp(mouse)
        self.__map.cancel_brewing(mouse)
        self.__map.add_water(mouse)
        self.__map.check_shaking()
        if self.__inventory.check_bankrupt(self.__map):
            # print('bankrupt')
            self.__state = 'restart'
        if self.__map.open_manual(mouse):
            self.__state = 'manual'

    def __run_shop(self, mouse):
        if not self.__customer_manager.startday:
            self.__customer_manager.startday = True
        self.__customer_manager.walk_away()
        if self.__customer_manager.current_customer is not None:
            if self.__customer_manager.startday:
                self.__customer_manager.walk_in()
            for key, v in self.__customer_manager.buttons.items():
                output = self.__customer_manager.check_click(mouse, key)
                if output == 'haggle':
                    self.__state = 'haggle'

        for slot in self.__inventory.slots:
            slot.check_click(mouse)
        self.__customer_manager.click_sent(mouse)

        self.__drawer.draw_shop_screen()

    def __run_haggle(self, mouse):
        self.__drawer.draw_shop_screen()
        self.__drawer.draw_haggle()
        self.__customer_manager.haggle.choose_difficulty(mouse)
        self.__customer_manager.doing_haggle()

        if self.__customer_manager.haggle.done:
            self.__customer_manager.done_haggle()
            self.__state = 'shop'

    def __run_title(self, mouse):
        self.__drawer.draw_title()
        if self.__drawer.play(mouse):
            self.__state = self.__prev_state
        if self.__drawer.open_stat(mouse):
            self.__root = tk.Tk()
            self.__data_display = DataApp(self.__root)
            self.__root.mainloop()

    def __run_tutorial(self):
        if self.__prev_state == 'map':
            self.__drawer.draw_brewing_screen()
        if self.__prev_state == 'bedroom':
            self.__drawer.draw_bedroom()
        if self.__prev_state == 'shop':
            self.__drawer.draw_shop_screen()

        self.__drawer.draw_tutorial()

    def __reset(self):
        self.__map.reset()
        self.__customer_manager.reset()
        self.__inventory.next_day()
        self.__inventory.save_data()

    def __check_tutorial(self):
        # print(self.__inventory.get_newbie())
        if self.__inventory.get_newbie():
            self.__state = 'tutorial'
            self.__inventory.not_newbie()


if __name__ == "__main__":
    name = input('Put ur name to log in: ')
    # name = 'anna'
    game = Game(name)
    game.run()
    pg.quit()
