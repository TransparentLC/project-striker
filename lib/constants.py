import os
import pathlib
import pygame

TITLE = 'Striker'
DATA_DIR = f'{pathlib.Path.home()}/.striker'

if os.path.exists('build-info.txt'):
    with open('build-info.txt', 'r', encoding='utf-8') as f:
        BUILD_INFO = f.read().splitlines()
else:
    BUILD_INFO = None

DEBUG_INPUT_DISPLAY_PRESSED = pygame.Color(255, 255, 0)
DEBUG_INPUT_DISPLAY_NOTPRESSED = pygame.Color(127, 127, 127)
DEBUG_HITBOX = pygame.Color(255, 255, 0)

PLAYER_SPEED_NORMAL = 4
PLAYER_SPEED_SLOW = 1.8

HOMING_ANGLE_RANGE = 2
BULLET_CANCELLING_INITIAL_REMAIN = 2

ITEM_GAIN_RANGE = 5
ITEM_MAGNET_RANGE = 50
ITEM_GET_BORDER = 112
GRAZE_RANGE = 20
HYPER_TIME = 480
HYPER_INVINCIBLE_TIME = 180

INITIAL_LIFENUM = 2
INITIAL_HYPERNUM = 3
