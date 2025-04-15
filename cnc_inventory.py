from typing import List

import pygame as pg
from cnc_config import Config
from cnc_potion import Potion
import math
import csv


class ItemSlot:
    def __init__(self, id, inv: "Inventory"):
        self.id = id
        self.item = None

        self.check_position()
        self.inv = inv
        self.box = pg.Rect(self.get_position()[0], self.get_position()[1], 95, 145)
        self.base = pg.image.load('IngamePic/Potion.png')
        self.base = pg.transform.scale(self.base, (70, 120))


    def get_position(self):
        return (self.x * 100) + 2, self.inv.upperline +  (self.y * 150 + 2)

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

    def draw(self, screen):
        self.box.topleft = self.get_position()
        pg.draw.rect(screen, Config.COLOR['map'], self.box, border_radius=5)
        if self.item is not None:
            screen.blit(self.base, (self.get_position()[0] + 12.5, self.get_position()[1] + 15))
            font = pg.font.SysFont('comicsansms', 20)
            text = font.render('I'*self.item.get_power(), True, Config.COLOR['marks'])
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
        self.__username = None
        self.__data = None

        self.__file = "cnc_save_test.csv"
        self.to_id(name)
        self.surface = pg.Surface((Config.INV_WIDTH, Config.INV_HEIGHT))

        self.upperline = 0
        self.slots = [ItemSlot(i + 1, self) for i in range(10)]
        self.next_id = 10 + 1
        for item in self.__inventory:
            self.add_to_slot(item)

        # moving up, down arrow
        self.arrowup_box = pg.Rect(Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT/2 - 50,
                                   40, 50)
        self.arrowdown_box = pg.Rect(Config.SCREEN_WIDTH - Config.INV_WIDTH - 40, Config.SCREEN_HEIGHT / 2 + 10,
                                   40, 50)

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

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
        print(inv)
        print(type(inv))
        for item in inv:
            self.__inventory.append(Potion(item['name'], (item['power']), item['ingredients']))
        return True

    def to_id(self, name: str):
        """
        if username not found, create new account
        :param name: username
        :return:
        """
        self.__username = name
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
            'Name': self.__username,
            'Days': str(self.__day),
            'Money': str(self.__money),
            'Inventory': self.str_inventory()
        }

        tmp_data = self.__data
        index = self.find_data(self.__username)
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
        return self.__username

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
        if 0 >= tmp >= (-150 * (self.next_id//2 - 4)):
            self.upperline = tmp
        # print(self.upperline)

    def check_arrow(self, mouse_pos):
        if pg.mouse.get_pressed()[0] == 1:
            if self.arrowup_box.collidepoint(mouse_pos):
                self.move_up_down(0.5)
            if self.arrowdown_box.collidepoint(mouse_pos):
                self.move_up_down(-0.5)



if __name__ == "__main__":
    inventory = Inventory()
    print(inventory.get_day())
    print(inventory.get_inventory())
    inventory.print_slot()
