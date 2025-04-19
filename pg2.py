from typing import List

import pygame as pg
from cnc_config import Config
import random

pg.init()

screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
running = True
rects_lst = []

press_pos = [0, 80]
move = 1
def draw_triangle(screen):
    pg.draw.polygon(screen, Config.COLOR['black'],
                    (press_pos, (press_pos[0]-10, 110), (press_pos[0]+10, 110)))

def move_triangle():
    global press_pos
    global move
    press_pos[0] += move * (1/5)
    if press_pos[0] > Config.SCREEN_WIDTH:
        move = -1
    if press_pos[0] < 0:
        move = 1

"""
creating the rect that wont intersect to any exist rect
"""


def create_rect():
    tmpr = pg.Rect((random.randint(0, Config.SCREEN_WIDTH - 7)), 50,
                   random.randint(30, 70), 50)
    while any(r.colliderect(tmpr) for r in rects_lst):
        tmpr = pg.Rect((random.randint(0, Config.SCREEN_WIDTH - 7)), 50,
                       random.randint(30, 70), 50)
    print('done')
    return tmpr


def checkrect(r:pg.Rect, pos):
    if r.collidepoint(pos):
            return True
    return False


while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_o:
                print("running")
                rects_lst.append(create_rect())
            if ev.key == pg.K_SPACE:
                for rect in rects_lst:
                    if checkrect(rect, press_pos):
                        rects_lst.remove(rect)
                        rects_lst.append(create_rect())
    screen.fill(Config.COLOR['map'])
    mouse = pg.mouse.get_pos()

    # print(rects_lst)
    move_triangle()
    for r in rects_lst:
        pg.draw.rect(screen, Config.COLOR['red'], r)
    pg.draw.circle(screen, Config.COLOR['green'], (20, 30), 2)
    draw_triangle(screen)



    pg.display.update()

    """
    pygame.Rect.collidelist
    test if one rectangle in a list intersects
    """
