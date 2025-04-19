import random
from typing import List

import pygame as pg
from cnc_config import Config
from cnc_potion import Potion
import math
import csv


class ItemSlot:
    def __init__(self, id, inv: "Inventory"):
        self.__enable = True
        self.id = id
        self.item = None

        self.check_position()
        self.inv = inv
        self.box = pg.Rect(self.get_position()[0], self.get_position()[1], 95, 145)
        self.hitbox = pg.Rect((Config.SCREEN_WIDTH - Config.INV_WIDTH) + self.get_position()[0],
                              Config.UI_HEIGHT + self.get_position()[1], 95, 145)
        self.base = pg.image.load('IngamePic/Potion.png')
        self.base = pg.transform.scale(self.base, (70, 120))

    def get_position(self):
        return (self.x * 100) + 2, self.inv.upperline + (self.y * 150 + 2)

    def is_empty(self):
        return self.item is None

    def check_position(self):
        self.y = math.ceil(self.id / 2) - 1
        self.x = 1 - (self.id % 2)

    def add_item(self, item: Potion):
        if self.is_empty():
            self.item = item
            return True
        return False

    def remove_item(self):
        self.item = None

    def get_item(self):
        item = self.item
        self.inv.remove_slot(self.id)  # self item will change
        return item

    def check_click(self, mouse_pos):
        if self.hitbox.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.__enable:
                self.__enable = False
                # print(self.item.__str__())
                self.inv.get_manager().offer(self.get_item())
        if pg.mouse.get_pressed()[0] == 0:
            self.__enable = True

    def draw(self, screen):
        self.box.topleft = self.get_position()
        self.hitbox.topleft = ((Config.SCREEN_WIDTH - Config.INV_WIDTH) + self.get_position()[0],
                               Config.UI_HEIGHT + self.get_position()[1])
        pg.draw.rect(screen, Config.COLOR['map'], self.box, border_radius=5)
        if self.item is not None:
            screen.blit(self.base, (self.get_position()[0] + 12.5, self.get_position()[1] + 15))
            font = pg.font.SysFont('comicsansms', 20)
            text = font.render('I' * self.item.get_power(), True, Config.COLOR['marks'])
            screen.blit(text, (self.get_position()[0] + 95 - 15 - (5 * self.item.get_power()),
                               self.get_position()[1] + 145 - 30))

    def __str__(self):
        if self.item is None:
            return f"{self.id}: None"
        return f"{self.id}: {self.item.__str__()}"


class Inventory:
    __instance = None

    def __new__(cls, para="lilly"):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__name = para

        return cls.__instance

    def __init__(self, name: str = 'lilly'):
        self.__day = None
        self.__money = None
        self.__inventory = []
        self.__name = None
        self.__data = None
        self.__manager: CustomerManager = None

        self.__file = "cnc_save_test.csv"
        self.to_id(name)
        self.surface = pg.Surface((Config.INV_WIDTH, Config.INV_HEIGHT))

        self.upperline = 0
        self.slots = [ItemSlot(i + 1, self) for i in range(10)]
        self.next_id = 10 + 1
        for item in self.__inventory:
            self.add_to_slot(item)

        # moving up, down arrow
        self.arrowup_box = pg.Rect(Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT / 2 - 50,
                                   40, 50)
        self.arrowdown_box = pg.Rect(Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT / 2 + 10,
                                     40, 50)

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def add_manager(self, manager: "CustomerManager"):
        if self.__manager is None:
            self.__manager = manager

    def get_manager(self):
        return self.__manager

    def __load_data(self) -> List[dict]:
        """
        get all data from csv file
        :return:
        """
        data = []
        with open(self.__file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data

    def __process(self, name) -> bool:
        """
        choose only one specific data to used
        :param name:
        :return bool: return False if there is no username yet
        """
        data = None
        for row in self.__data:
            if row['Name'] == name:
                data = row
        if data is None:
            return False
        self.__day = int(data['Days'])
        self.__money = float(data['Money'])
        inv = eval(data['Inventory'][1:-1])
        # print(inv)
        # print(type(inv))
        for item in inv:
            self.__inventory.append(Potion(item['name'], (item['power']), item['ingredients']))
        return True

    def to_id(self, name: str):
        """
        if username not found, create new account
        :param name: username
        :return:
        """
        self.__name = name
        self.__data = self.__load_data()

        if not self.__process(name):
            self.__inventory = []
            self.__money = 100
            self.__day = 1
            self.save_data()

    def find_data(self, name: str) -> int:
        """
        find data to save
        :param name:
        :return:
        """
        for row in self.__data:
            if row['Name'] == name:
                return self.__data.index(row)
        return -1

    def str_inventory(self) -> str:
        """
        make the inventory output that readable and re-use able
        :return str:
        """
        txt = '"['
        for item in self.__inventory:
            txt += item.__str__()
            if self.__inventory.index(item) != len(self.__inventory) - 1:
                txt += ','
        txt += ']"'
        return txt

    def save_data(self):
        """
        chang data into dict then rewrite to csv file
        :return:
        """
        # get data into dict
        tmp_row = {
            'Name': self.__name,
            'Days': str(self.__day),
            'Money': str(self.__money),
            'Inventory': self.str_inventory()
        }

        tmp_data = self.__data
        index = self.find_data(self.__name)
        if index != -1:
            tmp_data[index] = tmp_row
        else:
            tmp_data.append(tmp_row)

        # rewrite
        header = ["Name", "Days", "Money", "Inventory"]
        with open(self.__file, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for row in tmp_data:
                writer.writerow(row)

        self.__load_data()

    def get_name(self) -> str:
        return self.__name

    def get_slots(self):
        return self.slots

    def add_item(self, item):
        self.__inventory.append(item)
        self.add_to_slot(item)

    def add_to_slot(self, item: Potion):
        for slot in self.slots:
            if slot.is_empty():
                slot.add_item(item)
                return True

        if len(self.slots) % 2 == 0:  # Check if the number of slots is even
            new_slots = [ItemSlot(self.next_id + i) for i in range(2)]  # Create two new slots
            self.slots.extend(new_slots)
            self.next_id += 2
            self.slots[-2].add_item(item)  # Add the item to the first new slot
            return True
        return False

    def remove_slot(self, slot_id):
        if 1 <= slot_id <= len(self.slots):
            # Remove the item in the specified slot
            self.slots[slot_id - 1].remove_item()

            # Shift items to fill the gap
            for i in range(slot_id - 1, len(self.slots) - 1):
                self.slots[i].item = self.slots[i + 1].item
                self.slots[i].id = i + 1  # Update IDs
            self.slots[-1].remove_item()  # Last slot becomes empty
            return True
        return False

    def print_slot(self):
        for i in self.slots:
            print(i)

    def get_inventory(self):
        return self.__inventory

    def get_day(self):
        return self.__day

    def get_money(self) -> float:
        return self.__money

    def add_money(self, money: float):
        self.__money += money

    def deduct_money(self, money: float):
        self.__money -= money

    def move_up_down(self, num: int):
        tmp = self.upperline + (num * 10)
        if 0 >= tmp >= (-150 * (self.next_id // 2 - 4)):
            self.upperline = tmp
        # print(self.upperline)

    def check_arrow(self, mouse_pos):
        if pg.mouse.get_pressed()[0] == 1:
            if self.arrowup_box.collidepoint(mouse_pos):
                self.move_up_down(0.5)
            if self.arrowdown_box.collidepoint(mouse_pos):
                self.move_up_down(-0.5)


class Haggling:
    def __init__(self):
        self.movement = None
        self.surface = pg.Surface((400, 200))
        self.haggle_speed = (1 / 3)
        self.reset()

    def draw_triangle(self):
        pg.draw.polygon(self.surface, Config.COLOR['black'],
                        (self.haggle_pos,
                         (self.haggle_pos[0] - 10, self.haggle_pos[1] - 30),
                         (self.haggle_pos[0] + 10, self.haggle_pos[1] - 30)))

    def move_haggle(self):
        self.haggle_pos[0] += self.movement * self.haggle_speed
        if self.haggle_pos[0] > 380:
            self.movement = -1
        if self.haggle_pos[0] < 0:
            self.movement = 1

    def create_rect(self):
        tmpw = random.randint(20, 50)
        tmpr = pg.Rect((random.randint(0, 400 - tmpw)), 50,
                       tmpw, 50)
        while any(r.colliderect(tmpr) for r in self.hagglebar):
            tmpw = random.randint(20, 50)
            tmpr = pg.Rect((random.randint(0, 400 - tmpw)), 50,
                           tmpw, 50)
        return tmpr

    def check_haggle(self, r: pg.Rect):
        if r.collidepoint(self.haggle_pos):
            self.hagglebar.remove(r)
            self.hagglebar.append(r)
        return False

    def done(self):
        return self.multiplier

    def check_done(self):
        if self.multiplier <= 0.5:
            self.multiplier = 0.5
            return self.done()
        if self.multiplier >= 1.5:
            self.multiplier = 1.5
            return self.done()

    def reset(self):
        self.multiplier = 1
        self.hagglebar = []
        self.num_hagglebar = 5
        for i in range(self.num_hagglebar):
            self.hagglebar.append(self.create_rect())
        self.haggling_left = 30
        self.haggle_pos = [20, 80]
        self.movement = 1


class Customer:
    def __init__(self, rq, pic):
        self.__request = rq
        self.dialog = self.create_dialog().splitlines()
        self.pic = pg.image.load("customer/DemoCustomer.png")
        self.pic = pg.transform.scale(self.pic, (120, 333))
        self.patience = random.randint(1, 4)
        self.x = 10
        self.multiplier = 1

    def get_request(self):
        return self.__request

    def create_dialog(self):
        # first space bar after 30th letter
        tmplst = list(self.__request)
        for i in range(30, len(tmplst)):
            if tmplst[i] == ' ':
                tmplst[i] = '\n'
                break
            if tmplst[i] == '—':
                tmplst[i] = '—\n'
                break
        return ''.join(tmplst)


class CustomerManager:
    def __init__(self):
        self.__inventory = Inventory().get_instance()
        self.customers_each_day = random.randint(6, 10)
        self.num_customers = 0

        self.sell_pos = Config.SCREEN_WIDTH / 6

        self.current_customer = None
        self.prev_customer = None
        self.offered = None
        self.haggle = Haggling()
        self.create()
        self.startday = False
        self.dialogBox = pg.image.load("IngamePic/dialogBox.png")

        self.rejectButton = pg.Rect(430, 40 + 180, 150, 50)
        self.sellButton = pg.Rect(430 + 155, 40 + 180, 150, 50)
        self.haggleButton = pg.Rect(430 + 310, 40 + 180, 150, 50)
        self.buttons = {'Reject': [self.rejectButton, self.next_customer, False],
                        'Sell': [self.sellButton, self.sell, False],
                        'Haggle': [self.haggleButton, self.haggle, False], }

    @staticmethod
    def random_rq():
        key = list(Config.RQ.keys())
        ans = random.choice(key)
        return Config.RQ[ans][random.randint(0, len(Config.RQ[ans]) - 1)]

    @staticmethod
    def get_random_pic():
        file = random.choice(Config.customer_pic)
        pic = pg.image.load('IngamePic/' + file)
        pic = pg.transform.scale(pic, (30, 30))
        return pic

    def create(self):
        if self.num_customers < self.customers_each_day:
            self.current_customer = Customer(self.random_rq(), None)
            self.num_customers += 1
            return True
        self.current_customer = None
        return False

    def offer(self, potion: Potion):
        self.offered = potion
        self.check_offer()

    def walk_in(self):
        if self.current_customer.x < self.sell_pos:
            self.current_customer.x += 1
        else:
            self.buttons['Reject'][2] = True
            self.current_customer.x = self.sell_pos


    def check_offer(self):
        if self.current_customer.get_request() in Config.RQ[self.offered.get_name()]:
            self.buttons['Sell'][2] = True
            self.buttons['Haggle'][2] = True
            print("yes")
            # sell button and bargin enable
        else:
            self.current_customer.patience -= 1
            print("no")
            if self.current_customer.patience == 0:
                self.next_customer()

    def next_customer(self):
        self.prev_customer = self.current_customer
        self.create()
        return None

    def sell(self):
        self.__inventory.add_money(self.potion.get_price() * self.current_customer.multiplier)
        self.offered = None
        return None

    def haggle(self):
        return 'haggle'

    def check_click(self, mouse, key):
        output = None
        if self.buttons[key][0].collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.buttons[key][2]:
                self.buttons['Reject'][2] = False
                self.buttons['Haggle'][2] = False
                self.buttons['Sell'][2] = False
                print(key)
                output = self.buttons[key][1]()

        return output
