from cnc_config import Config


class DataCollector:
    __instance = None

    # database
    __filename = {
        'herb_use': 'herb_use.csv',
        'herb_potion': 'herb_each_potion.csv',
        'distance': 'potion_distance.csv',
        'sell_success': 'sell_success.csv',
        'haggle_fail': 'haggle_fail.csv',
    }

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance._connection = None
        return cls.__instance

    def __init__(self):
        self.reset()

    def end_day(self):
        self.__save_data()
        self.reset()

    def reset(self):
        self.__tmp_herbs_data = []
        self.__tmp_potions_data = []
        self.__tmp_distance_data = []
        self.__tmp_sell_data = []
        self.__tmp_haggle_data = []

    def __save_data(self):
        pass

    def add_data_herb(self, herb_list: list):
        for i in herb_list:
            self.__tmp_herbs_data.append[
                'Herb_name': Config.HERB_INFO[i]['name'],
                'Direction': Config.HERB_INFO[i]['direction'],
            ]
