import copy
import random
import time
from typing import List

import pygame as pg
from cnc_config import Config
from cnc_potion import Potion
from dataCollecting import DataCollector
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
            if pg.mouse.get_pressed()[0] == 1 and self.__enable and not self.is_empty():
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
            screen.blit(self.item.pic, (self.get_position()[0] + 12.5, self.get_position()[1] + 15))
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
        self.dataCollector = DataCollector()

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

        self.__data = self.__load_data()

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
            del self.__inventory[slot_id - 1]

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

    def next_day(self):
        self.save_data()
        self.dataCollector.end_day()
        self.__day += 1

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
    Haggle_WIN_W = 500
    Haggle_WIN_H = 300
    __difficulty = {
        1: {
            'speed': 1,
            'success': 0.05,
            'fail': 0.03,
            'reduce': 0.01
        },
        2: {
            'speed': 2,
            'success': 0.07,
            'fail': 0.04,
            'reduce': 0.02
        },
        3: {
            'speed': 3,
            'success': 0.07,
            'fail': 0.04,
            'reduce': 0.02
        }
    }

    def __init__(self):
        self.__level = 1
        self.set_difficulty(self.__level)
        self.movement = None
        self.__dataCollector = DataCollector()
        self.surface = pg.Surface((self.Haggle_WIN_W, self.Haggle_WIN_H))
        self.surfaceR = self.surface.get_rect()
        self.reset()
        self.done_rect = [pg.Rect(10, 150, 40, 50), pg.Rect(self.Haggle_WIN_W - 50, 150, 40, 50)]
        self.done = False
        self.timer = time.time()

        self.details = pg.image.load('IngamePic/DealDetails.png')
        self.details = pg.transform.scale(self.details, (225, 145))
        self.difficulty_button = {
            1: pg.Rect(2, 2, 91, 145),
            2: pg.Rect(93, 2, 91, 145),
            3: pg.Rect(184, 2, 91, 145),
        }
        self.difficulty_hitbox = {
            1: pg.Rect(2 + 400, 2 + 100, 91, 145),
            2: pg.Rect(93 + 400, 2 + 100, 91, 145),
            3: pg.Rect(184 + 400, 2 + 100, 91, 145),
        }

    def get_level(self):
        return self.__level

    def set_difficulty(self, difficulty):
        self.__level = difficulty
        self.__haggle_speed = self.__difficulty[difficulty]['speed']
        self.__success_add = self.__difficulty[difficulty]['success']
        self.__fail_add = self.__difficulty[difficulty]['fail']
        self.__reduce_add = self.__difficulty[difficulty]['reduce']

    def draw_triangle(self):
        pg.draw.polygon(self.surface, Config.COLOR['black'],
                        (self.haggle_pos,
                         (self.haggle_pos[0] - 10, self.haggle_pos[1] + 30),
                         (self.haggle_pos[0] + 10, self.haggle_pos[1] + 30)))

    def choose_difficulty(self, mouse):
        # print('choose difficulty')
        for dif, r in self.difficulty_hitbox.items():
            if r.collidepoint(mouse):
                if pg.mouse.get_pressed()[0] == 1:
                    # print(dif)
                    self.set_difficulty(dif)

    def move_haggle(self):
        """
        move the triangle left and right
        """
        self.haggle_pos[0] += self.movement * self.__haggle_speed
        if self.haggle_pos[0] > self.Haggle_WIN_W - 15:
            self.movement = -1
        if self.haggle_pos[0] < 15:
            self.movement = 1

    def create_rect(self) -> pg.Rect:
        """
        Create Random size rect that doesn't collide to other rect created

        :return: pg.Rect object; random size rectangle
        """
        tmpw = random.randint(20, 60)
        tmpr = pg.Rect((random.randint(50, self.Haggle_WIN_W - 50 - tmpw)), 150,
                       tmpw, 50)
        while any(r.colliderect(tmpr) for r in self.hagglebar):
            tmpw = random.randint(20, 50)
            tmpr = pg.Rect((random.randint(50, self.Haggle_WIN_W - 50 - tmpw)), 150,
                           tmpw, 50)
        return tmpr

    def check_haggle(self, r: pg.Rect):
        """
        Check if the haggle rectangle was clicked
        """
        if r.collidepoint(self.haggle_pos):
            self.hagglebar.remove(r)
            self.hagglebar.append(self.create_rect())
            return True
        return False

    def haggle_action(self):
        """
        As the button is press, check every haggle bar if it's clicked
        if yes + 0.05
        if no - 0.03 and collect the data
        TODO: collect haggle data here
        """
        success = False
        for r in self.hagglebar:
            if self.check_haggle(r):
                self.multiplier += self.__success_add
                success = True
        else:
            self.multiplier -= self.__fail_add
        self.__dataCollector.add_haggle_data(self.num_hagglebar,
                                             self.__haggle_speed,
                                             success)

    def reduce_overtime(self):
        """
        make when the time goes by the multiplier is reduced; 0.005 per 0.5s
        """
        t = time.time()
        if t - self.timer >= 0.5:
            self.multiplier -= self.__reduce_add
            self.timer = t

    def click_done(self):
        """
        Check if the done (green rectangle) was clicked
        """
        for r in self.done_rect:
            if r.collidepoint(self.haggle_pos):
                self.done = True

    def check_auto_done(self):
        """
        if the haggling is huge success or lose, end it automatically

        :return bool: True or False:
        """
        if self.multiplier <= 0.5:
            self.multiplier = 0.5
            self.done = True
            return self.done
        if self.multiplier >= 1.5:
            self.multiplier = 1.5
            self.done = True
            return self.done
        if self.start:
            self.reduce_overtime()
        return False

    def reset(self):
        """
        reset haggle every time it is called
        """
        self.multiplier = 1
        self.hagglebar = []
        self.num_hagglebar = 5
        for i in range(self.num_hagglebar):
            self.hagglebar.append(self.create_rect())
        self.haggling_left = 30
        self.haggle_pos = [20, 180]
        self.movement = 1
        self.done = False
        self.start = False


class Customer:
    def __init__(self, rq, pic):
        self.__request = rq
        self.dialog = self.create_dialog().splitlines()
        self.pic = pg.image.load("customer/DemoCustomer.png")
        self.pic = pg.transform.scale(self.pic, (120, 333))
        self.patience = random.randint(3, 10)
        self.x = 10
        self.multiplier = 1 * round((random.randint(1, 10)/50), 2)

    def get_request(self):
        return self.__request

    def create_dialog(self) -> str:
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
        self.__dataCollector = DataCollector()
        self.sell_pos = Config.SCREEN_WIDTH / 6

        self.customers_each_day = random.randint(6, 10)
        self.num_customers = 0
        self.current_customer = None
        self.prev_customer = None
        # self.offered = Potion('STONE', 3, [])
        self.offered = None
        self.create()
        self.startday = False

        self.offering_hitbox = pg.Rect(720, 420, 120, 180)  # +25 +30
        self.haggle = Haggling()
        self.dialogBox = pg.image.load("IngamePic/dialogBox.png")

        self.rejectButton = pg.Rect(430, 40 + 180, 150, 50)
        self.sellButton = pg.Rect(430 + 155, 40 + 180, 150, 50)
        self.haggleButton = pg.Rect(430 + 310, 40 + 180, 150, 50)
        self.buttons = {'Reject': [self.rejectButton, self.next_customer, False],
                        'Sell': [self.sellButton, self.sell, False],
                        'Haggle': [self.haggleButton, self.sent_haggle, False], }

        self.cashier = self.add_picture('Cashier.png', (400, 228))

        self.trail = 1

    @staticmethod
    def add_picture(filename: str, size: tuple):
        pic = pg.image.load('IngamePic/' + filename)
        pic = pg.transform.scale(pic, size)
        return pic

    def reset(self):
        self.customers_each_day = random.randint(6, 10)
        self.num_customers = 0
        self.current_customer = None
        self.prev_customer = None
        self.offered = None
        self.create()
        self.startday = False

        self.buttons['Reject'][2] = False
        self.buttons['Sell'][2] = False
        self.buttons['Haggle'][2] = False

    def random_rq(self):
        key = list(Config.RQ.keys())
        weight = [3, 1, 2, 1, 6, 2, 6, 3, 3, 1, 2, 1, 6, 3, 6, 2]
        ans = random.choices(key, weights=weight)[0]
        rq = Config.RQ[ans][random.randint(0, len(Config.RQ[ans]) - 1)]
        if self.prev_customer is not None:
            while rq == self.prev_customer.get_request():
                Config.RQ[ans][random.randint(0, len(Config.RQ[ans]) - 1)]
        return rq

    @staticmethod
    def get_random_pic():
        file = random.choice(Config.customer_pic)
        pic = pg.image.load('IngamePic/' + file)
        pic = pg.transform.scale(pic, (30, 30))
        return pic

    def create(self):
        """
        create a new customer as long as the customer create is not reach amount of customer per day
        """
        # TODO: pic = get_random_pic()
        if self.num_customers < self.customers_each_day:
            self.current_customer = Customer(self.random_rq(), None)
            self.num_customers += 1
            return True
        self.current_customer = None
        return False

    def offer(self, potion: Potion):
        """
        make an offered to the customer
        """
        self.offered = potion
        self.check_offer()
        self.current_customer.multiplier = 1

    def walk_in(self):
        """
        walk in slowly until reach the point then activate the buttons
        """
        if self.current_customer.x < self.sell_pos:
            self.current_customer.x += 1
        else:
            self.buttons['Reject'][2] = True
            self.current_customer.x = self.sell_pos

    def check_offer(self):
        """
        check if offer is satisfied, if not for too many times they will walk away
        """
        if self.current_customer.get_request() in Config.RQ[self.offered.get_name()]:
            self.buttons['Sell'][2] = True
            self.buttons['Haggle'][2] = True
        else:
            self.current_customer.patience -= 1
            self.trail += 1
            if self.current_customer.patience == 0:
                self.next_customer(False)

    def walk_away(self):
        """
        walk away animation
        """
        if self.prev_customer is not None:
            if self.prev_customer.x < Config.SCREEN_WIDTH:
                self.prev_customer.x += 3
            else:
                self.prev_customer = None

    def next_customer(self, success=False):
        """
        move the customer to prev for animation and create new one
        """
        self.prev_customer = self.current_customer
        self.create()
        self.__dataCollector.add_sell_data(success, self.trail)
        self.trail = 1

        return None

    def sell(self):
        """
        sell: add money, remove item and call next customer
        """
        self.__inventory.add_money(self.offered.get_price() * self.current_customer.multiplier)
        self.offered = None
        self.next_customer(True)
        return None

    def sent_haggle(self):
        """
        activate haggle by sent the str to main
        """
        self.haggle.reset()
        print('HAGGLE')
        return 'haggle'

    def doing_haggle(self):
        """
        make sure that the haggle is working
        """
        done = self.haggle.check_auto_done()
        # print('Done: ',done)
        if not done:
            self.haggle.move_haggle()

    def done_haggle(self):
        """
        reactivate the button after done haggle
        """
        self.buttons['Sell'][2] = True
        self.buttons['Reject'][2] = True
        self.current_customer.multiplier *= self.haggle.multiplier

    def check_click(self, mouse, key):
        """
        check if the button was clicked
        """
        output = None
        condition = None
        if self.buttons[key][0].collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.buttons[key][2]:
                self.buttons['Reject'][2] = False
                self.buttons['Haggle'][2] = False
                self.buttons['Sell'][2] = False
                print(key)
                output = self.buttons[key][1]()

        return output

    def offered_not_none(self):
        """
        check if the offer is none
        """
        return self.offered is not None

    def draw_offering(self, screen):
        """
        draw the offering
        """
        # pg.draw.rect(screen, Config.COLOR['black'],self.offering_hitbox)
        if self.offered is not None:
            pic = pg.transform.scale(self.offered.pic, (100, 170))
            screen.blit(pic, (self.offering_hitbox.x + 10, self.offering_hitbox.y + 5))

    def click_sent(self, mouse):
        if self.offering_hitbox.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.offered_not_none():
                self.sent_back()

    def sent_back(self):
        """
        send back the offer to inventory
        """
        self.__inventory.add_item(self.offered)
        self.offered = None

    def get_price(self):
        return self.offered.get_price() * self.haggle.multiplier
