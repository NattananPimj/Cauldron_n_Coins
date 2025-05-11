from cnc_game import Game
from cnc_config import Config
import pygame as pg

# ADDITIONAL Setting

Config.MUSIC_VOLUME = 0.2


if __name__ == "__main__":
    name = input('Put ur name to log in: ')
    game = Game(name)
    game.run()
    pg.quit()