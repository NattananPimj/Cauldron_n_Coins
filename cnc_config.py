import pygame as pg

class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    MAP_WIDTH = 1000
    MAP_HEIGHT = 600
    ORIGIN_X = 600
    ORIGIN_Y = 350
    FACTOR_x = 1/20 # each block

    COLOR = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0)
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

        }
        ]
    
    POTION_POS = {
        "SWIFTNESS":(10, 220),
        "DEXITY":(120, 270),
        "MANA": (210, 180),
        "EXPLOSION": (250, 130),
        "FIRE": (300, 25),
        "LIGHT": (350, -50),
        "HEAL": (200, -150),
        "GROWTH":(100, -200),
        "STRENGHT":(15, -190),
        "STONE": (-150, -220),
        "SLEEP": (-230, -180),
        "SLOW":(-350, -120),
        "FROST": (-300, -55),
        "LIGHTNING":(-280, 8),
        "POISON": (-230, 120),
        "RAGE":(-120, 250)
    }