from typing import List

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
        self.__day = None
        self.__money = None
        self.__inventory = []
        self.__username = None
        self.__data = None

        self.__file = "cnc_save_test.csv"
        self.to_id(name)

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


if __name__ == "__main__":
    inventory = Inventory("b")
    print(inventory.get_day())
    print(inventory.get_inventory())
    inventory.save_data()
