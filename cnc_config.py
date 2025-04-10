import math


class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    MAP_WIDTH = 700
    MAP_HEIGHT = 400
    HERB_WIDTH = 200
    HERB_HEIGHT = 640
    FACTOR_x = 1 / 20  # each block
    MOVESPEED = 40  # the bigger the slower

    COLOR = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'background': (212, 198, 169),
        'map': (212, 188, 159),
        'path': (94, 90, 78),
        'marks': (100, 100, 100)
    }
    '''
    HERB PATTERN
        'name': ''
        'direction': '' # N E W S NE NW SE SW
        'func': '' # lamda x: func(x)
        'picture': ''
    '''

    POTION_POS = {
        "SWIFTNESS": (10, 650),
        "DEXITY": (400, 750),
        "MANA": (525, 450),
        "EXPLOSION": (800, 320),
        "FIRE": (450, 25),
        "LIGHT": (820, -50),
        "HEAL": (200, -150),
        "GROWTH": (250, -570),
        "STRENGTH": (15, -500),
        "STONE": (-400, -800),
        "SLEEP": (-500, -500),
        "SLOW": (-800, -205),
        "FROST": (-450, -70),
        "LIGHTNING": (-500, 350),
        "POISON": (-200, 200),
        "RAGE": (-500, 600)
    }

    POTION_info = {
        "SWIFTNESS": {
            'pic': '',
            'price': 0,
        },
        "DEXITY": {
            'pic': '',
            'price': 0,
        },
        "MANA": {
            'pic': '',
            'price': 0,
        },
        "EXPLOSION": {
            'pic': '',
            'price': 0,
        },
        "FIRE":{
            'pic': '',
            'price': 0,
        },
        "LIGHT": {
            'pic': '',
            'price': 0,
        },
        "HEAL": {
            'pic': '',
            'price': 0,
        },
        "GROWTH": {
            'pic': '',
            'price': 0,
        },
        "STRENGTH": {
            'pic': '',
            'price': 0,
        },
        "STONE": {
            'pic': '',
            'price': 0,
        },
        "SLEEP": {
            'pic': '',
            'price': 0,
        },
        "SLOW":{
            'pic': '',
            'price': 0,
        },
        "FROST": {
            'pic': '',
            'price': 0,
        },
        "LIGHTNING": {
            'pic': '',
            'price': 0,
        },
        "POISON": {
            'pic': '',
            'price': 0,
        },
        "RAGE":{
            'pic': '',
            'price': 0,
        }
    }

    HERB_INFO = {
        '01': {
            'name': '',
            'funcX': lambda t: 5 * t + 10 * math.cos(t),
            'funcY': lambda t: 10 * math.sin(t),
            't': 75,
            'direction': 'E',
            'pic': 'H01.JPG'
        },

        '02': {
            'name': '',
            'funcX': lambda t: 5 * t,
            'funcY': lambda t: 10 * math.sin(t/2),
            't': 50,
            'direction': 'E',
            'pic': 'H02.JPG'
        },

        '03': {
            'name': '',
            'funcX': lambda t: 5 * t,
            'funcY': lambda t: 10 * (t/2 + abs((t/2 % 5) - 2.5)),
            't': 40,
            'direction': 'NE',
            'pic': 'H03.JPG'
        },

        '04': {
            'name': '',
            'funcX': lambda t: (2 * t) + 10 * math.cos(t),
            'funcY': lambda t: (5 * t) + -15 * math.sin(t),
            't': 40,
            'direction': 'NE',
            'pic': 'H04.JPG'
        },

        '05': {
            'name': '',
            'funcX': lambda t: t/2 * math.cos(t/2),
            'funcY': lambda t: 5 * (t + math.cos(t)),
            't': 50,
            'direction': 'N',
            'pic': 'H05.JPG'
        },

        '06': {
            'name': '',
            'funcX': lambda t: 10 * abs((t/2 % 5) - 2.5),
            'funcY': lambda t: 5 * t,
            't': 40,
            'direction': 'N',
            'pic': 'H06.JPG'
        },

        '07': {
            'name': '',
            'funcX': lambda t: -5*t,
            'funcY': lambda t: (2*t) - 10*abs(math.sin(t/5)),
            't': int(15*math.pi),
            'direction': 'NW',
            'pic': 'H07.JPG'
        },

        '08': {
            'name': '',
            'funcX': lambda t: (-2 * t) - 10 * math.cos(t),
            'funcY': lambda t: (5 * t) + -15 * math.sin(t),
            't': 50,
            'direction': 'NW',
            'pic': 'H08.JPG'
        },

        '09': {
            'name': '',
            'funcX': lambda t: (-4*t) - 10*math.sin(t),
            'funcY': lambda t: 10 * math.cos(t/2),
            't': 50,
            'direction': 'W',
            'pic': 'H09.JPG'
        },

        '10': {
            'name': '',
            'funcX': lambda t: -5 * t,
            'funcY': lambda t: 10 * math.sin(t/2),
            't': 50,
            'direction': 'W',
            'pic': 'H10.JPG'
        },

        '11': {
            'name': '',
            'funcX': lambda t: 100 * math.sin(t/8),
            'funcY': lambda t: 40 * math.cos(t/8),
            't': 40,
            'direction': 'SW',
            'pic': 'H11.JPG'
        },

        '12': {
            'name': '',
            'funcX': lambda t: t,
            'funcX': lambda t: 5 * t,
            'funcY': lambda t: 10 * (t / 2 + abs((t / 2 % 5) - 2.5)),
            't': 40,
            'direction': 'SW',
            'pic': 'H12.JPG'
        },

        '13': {
            'name': '',
            'funcX': lambda t: 10 * math.sin(t/2),
            'funcY': lambda t: 100 * math.cos(t/10),
            't': 40,
            'direction': 'S',
            'pic': 'H13.JPG'
        },

        '14': {
            'name': '',
            'funcX': lambda t: 20 * math.sin(t/2),
            'funcY': lambda t: (-5 * t) + (10*math.cos(t)),
            't': 50,
            'direction': 'S',
            'pic': 'H14.JPG'
        },

        '15': {
            'name': '',
            'funcX': lambda t: (10 * math.sin(t/3))-t,
            'funcY': lambda t: 4 - (((t-2)**2)/25),
            't': 50,
            'direction': 'SE',
            'pic': 'H15.JPG'
        },

        '16': {
            'name': '',
            'funcX': lambda t: -5 * t + 10 * math.cos(t),
            'funcY': lambda t: -5*t + 10 * math.sin(t),
            't': 50,
            'direction': 'SE',
            'pic': 'H16.JPG'
        },
    }
