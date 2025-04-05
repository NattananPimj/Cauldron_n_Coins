
class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    MAP_WIDTH = 800
    MAP_HEIGHT = 400
    FACTOR_x = 1 / 20  # each block

    COLOR = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'background': (212, 198, 169),
        'map': (212, 188, 159),
        'path': (94, 90, 78),
        'marks' :(100, 100, 100)
    }
    '''
    HERB PATTERN
        'name': ''
        'direction': '' # N E W S NE NW SE SW
        'func': '' # lamda x: func(x)
        'picture': ''
    '''
    HERB = [
        {
            'name': '',
            'direction': 'E',
            'func': '',
            'picture': ''
        },
        {
            'name': '',
            'direction': 'E',
            'func': '',
            'picture': ''
        }
    ]

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
