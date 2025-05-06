import pygame as pg
from pygame import mixer
from cnc_herbs import *
from cnc_classes import *
from cnc_config import Config
from cnc_inventory import Inventory, CustomerManager
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
        self.__customer_manager = CustomerManager()
        self.__inventory.add_manager(self.__customer_manager)
        self.__map = Map()
        self.__herbs = HerbManager(self.__map)
        self.__drawer = Drawer(self.__map, self.__herbs, self.__customer_manager)
        self.__state = 'shop'  # map / store
        self.__prev_state = 'map'
        self.__music_file = 'Music/misty-wind-troubadour-164146.ogg'

        self.__running = True

    def user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__running = False
            if ev.type == pg.MOUSEWHEEL:
                self.__inventory.move_up_down(ev.y)
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.__state = 'title'

                if self.__state == 'map':
                    if ev.key == pg.K_LEFT:
                        self.__state = 'shop'
                    if ev.key == pg.K_UP:
                        self.__state = 'bedroom'
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

                if self.__state == 'haggle':
                    if ev.key == pg.K_SPACE:
                        # temporary
                        self.__customer_manager.haggle.start = True
                        self.__customer_manager.haggle.haggle_action()
                        self.__customer_manager.haggle.click_done()
                        # print(self.__customer_manager.haggle.multiplier)

                if self.__state == 'bedroom':
                    if ev.key == pg.K_DOWN:
                        self.__state = self.__prev_state

        # hold key down
        key = pg.key.get_pressed()
        # self.move_to_origin()
        if key[pg.K_SPACE]:
            self.__map.back_to_origin()
        self.__map.move_map(key)

    def run(self):
        self.music()
        while self.__running:
            """
            user event + checking mouse clicking
            """
            mouse = pg.mouse.get_pos()
            self.user_event()
            self.__inventory.check_arrow(mouse)

            if self.__state == 'map':
                self.__drawer.draw_brewing_screen()
                for block in self.__herbs.herb_blocks:
                    block.check_hover(mouse, self.__drawer.get_screen())
                    block.check_click(mouse)
                self.__map.brewing(mouse)
                self.__map.bottlingUp(mouse)
                self.__map.cancel_brewing(mouse)
                self.__map.add_water(mouse)
                if self.__map.open_manual(mouse):
                    self.__state = 'manual'

            if self.__state == 'manual':
                self.__drawer.draw_brewing_screen()
                self.__drawer.draw_manual()

            if self.__state == 'shop':
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
                # print(self.__customer_manager.buttons['Sell'][2])

                for slot in self.__inventory.slots:
                    slot.check_click(mouse)
                self.__customer_manager.click_sent(mouse)

                self.__drawer.draw_shop_screen()

            if self.__state == 'bedroom':
                self.__drawer.draw_bedroom()
                if self.__drawer.check_sleep(mouse):
                    self.reset()

            if self.__state == 'haggle':
                self.__drawer.draw_shop_screen()
                self.__drawer.draw_haggle()
                self.__customer_manager.haggle.choose_difficulty(mouse)
                self.__customer_manager.doing_haggle()

                if self.__customer_manager.haggle.done:
                    self.__customer_manager.done_haggle()
                    self.__state = 'shop'

            if self.__state == 'title':
                self.__drawer.draw_title()

            pg.display.update()


    def music(self):
        mixer.init()
        mixer.music.load(self.__music_file)
        mixer.music.play(-1)
        mixer.music.set_volume(Config.MUSIC_VOLUME)

    def reset(self):
        self.__map.reset()
        self.__customer_manager.reset()
        self.__inventory.next_day()
        self.__inventory.save_data()


if __name__ == "__main__":
    # name = input('Put ur name to log in: ')
    name = 'lilly'
    game = Game(name)
    game.run()
