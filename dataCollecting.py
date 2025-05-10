from cnc_config import Config
import csv


class DataCollector:
    __instance = None

    # database
    __filename = {
        'herb_use': 'herb_use.csv',
        'potion_profit': 'potion_profit.csv',
        'distance': 'potion_distance.csv',
        'sell_success': 'sell_success.csv',
        'haggle_fail': 'haggle_fail.csv',
    }
    __header = {
        'herb_use': ['ID', 'Herb_name', 'Direction'],
        'potion_profit': ['Potion','Sellprice','Cost','Profit'],
        'distance': ['Potion', 'Tier', 'Distance'],
        'sell_success': ['Success', 'Trial'],
        'haggle_fail': ['Number_of_bar', 'Speed', 'Success'],
    }

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance._connection = None
        return cls.__instance

    def __init__(self):
        self.__herbs_data = []
        self.__potions_data = []
        self.__distance_data = []
        self.__sell_data = []
        self.__haggle_data = []
        self.__data = {
            'herb_use': self.__herbs_data,
            'potion_profit': self.__potions_data,
            'distance': self.__distance_data,
            'sell_success': self.__sell_data,
            'haggle_fail': self.__haggle_data,
        }

    def end_day(self):
        for key in self.__data.keys():
            self.__save_data(key, self.__data[key])
        self.reset()

    def reset(self):
        for value in self.__data.values():
            value.clear()

    def add_data_herb(self, herb_list: list):
        for i in herb_list:
            self.__herbs_data.append({
                'ID': i,
                'Herb_name': Config.HERB_INFO[i]['name'],
                'Direction': Config.HERB_INFO[i]['direction'],
            })

    def add_potion_data(self, potion, sellprice, cost):
        self.__potions_data.append({
            'Potion': potion,
            'Sellprice': sellprice,
            'Cost': cost,
            'Profit': sellprice - cost,
        })

    def add_distance_data(self, potion, tier, distance):
        self.__distance_data.append({
            'Potion': potion,
            'Tier': tier,
            'Distance': distance,
        })

    def add_sell_data(self, success, trial):
        self.__sell_data.append({
            'Success': success,
            'Trial': trial,
        })

    def add_haggle_data(self, bar, speed, success):
        self.__haggle_data.append({'Number_of_bar': bar,
                                   'Speed': speed,
                                   'Success': success
                                   })

    def __save_data(self, f, data):
        tmp = []
        with open('database/' + self.__filename[f], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tmp.append(row)

        tmp.extend(data)
        header = self.__header[f]
        with open('database/' + self.__filename[f], 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for row in tmp:
                writer.writerow(row)