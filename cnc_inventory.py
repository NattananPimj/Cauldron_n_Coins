import pygame as pg
from cnc_config import Config
from cnc_potion import Potion
import math
import csv


class Inventory:
    __instance = None

    def __new__(cls, para="lilly"):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__name = para

        return cls.__instance

    def __init__(self, name: str = 'lilly'):
        """
        TODO:
              2. make the init read data from csv and sent data back every time game save
              3. if there is new people, create new acc
        """
        self.__day = None
        self.__money = None
        self.__inventory = []
        self.__username = None

        self.__file = "cnc_save_test.csv"
        self.data = self.load_data()
        self.to_id(name)

    def load_data(self):
        data = []
        with open(self.__file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data

    def process(self, name):
        data = None
        for row in self.data:
            if row['Name'] == name:
                data = row
        if data is None:
            return False
        self.__day = int(data['Days'])
        self.__money = float(data['Money'])
        inv = eval(data['Inventory'])
        for item in inv:
            self.__inventory.append(Potion(item['name'], item['power'], item['ingredients']))
        return True

    def to_id(self, name: str):
        self.__username = name
        self.data = self.load_data()

        if not self.process(name):
            self.__inventory = []
            self.__money = 0
            self.__day = 1
            self.game_save()

    def save_data(self):
        pass

    def add_item(self, item):
        self.__inventory.append(item)

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

    def game_save(self):
        # rewrite data in csv
        pass


if __name__ == "__main__":
    inventory = Inventory()
    print(inventory.load_data())
    print(inventory.get_inventory())
