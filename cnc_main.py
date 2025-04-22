import pygame as pg
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
        self.__state = 'map'  # map / store
        self.__prev_state = 'map'

        self.__running = True

    def user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__running = False
            if ev.type == pg.MOUSEWHEEL:
                self.__inventory.move_up_down(ev.y)
            if ev.type == pg.KEYDOWN:

                if self.__state == 'map':
                    if ev.key == pg.K_LEFT:
                        self.__state = 'shop'
                    if ev.key == pg.K_UP:
                        self.__state = 'bedroom'
                        self.__prev_state = 'map'

                if self.__state == 'shop':
                    if ev.key == pg.K_RIGHT:
                        self.__state = 'map'
                    if ev.key == pg.K_UP:
                        self.__state = 'bedroom'
                        self.__prev_state = 'shop'

                if self.__state == 'haggle':
                    if ev.key == pg.K_SPACE:
                        # temporary
                        # TODO: keep it inside haggle/customer manager + make satus that done or not done haggling
                        for bar in self.__customer_manager.haggle.hagglebar:
                            if self.__customer_manager.haggle.check_haggle(bar):
                                self.__customer_manager.haggle.multiplier += 0.05
                        else:
                            self.__customer_manager.haggle.multiplier -= 0.03
                        self.__customer_manager.haggle.multiplier -= 0.01
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

                for slot in self.__inventory.slots:
                    slot.check_click(mouse)
                self.__customer_manager.click_sent(mouse)

                self.__drawer.draw_shop_screen()

            if self.__state == 'bedroom':
                self.__drawer.draw_bedroom()

            if self.__state == 'haggle':
                self.__drawer.draw_shop_screen()
                self.__drawer.draw_haggle()
                self.__customer_manager.doing_haggle()

            pg.display.update()


if __name__ == "__main__":
    # name = input('Put ur name to lock in: ')
    name = 'lilly'
    game = Game(name)
    game.run()
