import os
import pygame

import lib.constants
import lib.globals
import lib.newgame
import lib.replay
import lib.sound
import lib.utils

from .title import BACKGROUND
from .title import MENU_ITEMS

OPTION = pygame.image.load(lib.utils.getResourceHandler('assets/ui-title-select.webp')).convert_alpha()
OPTION_ITEMS = tuple(OPTION.subsurface((0, x * 256, 768, 256)) for x in range(3))

import lib.scene.stg
import lib.scene.title

optionChoice = 0

def update():
    global optionChoice

    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()
    elif (
        (lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]) or
        (lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP])
    ):
        optionChoice = (optionChoice - 1) % 3
        lib.sound.sfx['PAGE'].play()
    elif (
        (lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]) or
        (lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN])
    ):
        optionChoice = (optionChoice + 1) % 3
        lib.sound.sfx['PAGE'].play()
    elif lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.globals.optionType = optionChoice
        lib.globals.stgRandomSeed = os.urandom(8)
        lib.newgame.init()
        lib.replay.startRecording()

def draw(surface: pygame.Surface):
    surface.blit(BACKGROUND, (0, 0))
    surface.blit(MENU_ITEMS[0][0], (640 - MENU_ITEMS[0][0].get_width() // 2, 64))
    for index, item in enumerate(OPTION_ITEMS):
        item.set_alpha(255 if index == optionChoice else 127)
        surface.blit(item, (128 + 128 * index, 128 + 270 * index))
