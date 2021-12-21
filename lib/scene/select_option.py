import pygame

import lib.constants
import lib.globals
import lib.script_engine.stage
import lib.sound
import lib.sprite.option
import lib.stg_overlay

from .title import BACKGROUND
from .title import MENU_ITEMS

OPTION = pygame.image.load('assets/ui-title-select.webp').convert_alpha()
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
        lib.globals.groupPlayer.sprite.position.update(192, 400)
        lib.globals.groupPlayer.sprite.invincibleRemain = 0
        lib.globals.groupPlayer.sprite.hyperRemain = 0
        lib.globals.groupPlayer.sprite.deathWait = 0
        lib.globals.score = 0
        lib.globals.scoreLastFrame = 0
        lib.globals.grazeCount = 0
        lib.globals.maxGetPoint = 10000
        lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM
        lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
        lib.globals.missedCount = 0
        lib.globals.hyperUsedCount = 0
        lib.globals.continueCount = 0
        lib.globals.continueRemain = 0
        lib.globals.continueEnabled = True
        lib.globals.allCleared = False
        for i in range(len(lib.stg_overlay.overlayStatus)):
            lib.stg_overlay.overlayStatus[i] = 0
        for g in (
            lib.globals.groupPlayerOption,
            lib.globals.groupPlayerBullet,
            lib.globals.groupEnemy,
            lib.globals.groupEnemyBullet,
            lib.globals.groupParticle,
            lib.globals.groupItem,
        ):
            for s in g:
                s.kill()
        lib.globals.optionType = optionChoice

        if optionChoice == 0:
            lib.globals.groupPlayer.sprite.options = [
                lib.sprite.option.OptionTypeA(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
                lib.sprite.option.OptionTypeA(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
                lib.sprite.option.OptionTypeA(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
                lib.sprite.option.OptionTypeA(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
            ]
        elif optionChoice == 1:
            lib.globals.groupPlayer.sprite.options = [
                lib.sprite.option.OptionTypeB1(8, pygame.Vector2(-15, 20), pygame.Vector2(-25, 0), 12, 0),
                lib.sprite.option.OptionTypeB0(8, pygame.Vector2(15, 20), pygame.Vector2(25, 0), -12, 0),
                lib.sprite.option.OptionTypeB0(8, pygame.Vector2(-30, 5), pygame.Vector2(-45, 0), 30, 0),
                lib.sprite.option.OptionTypeB1(8, pygame.Vector2(30, 5), pygame.Vector2(45, 0), -30, 0),
            ]
        elif optionChoice == 2:
            lib.globals.groupPlayer.sprite.options = [
                lib.sprite.option.OptionTypeC(8, pygame.Vector2(-25, 0), pygame.Vector2(-10, -15), 0, 0),
                lib.sprite.option.OptionTypeC(8, pygame.Vector2(25, 0), pygame.Vector2(10, -15), 0, 0),
            ]

        with open('scriptfiles/stage/stage1.txt', 'r', encoding='utf-8') as f:
            lib.globals.stageEngine = lib.script_engine.stage.Engine(f.read())
        lib.globals.nextScene = lib.scene.stg

def draw(surface: pygame.Surface):
    surface.blit(BACKGROUND, (0, 0))
    surface.blit(MENU_ITEMS[0][0], (640 - MENU_ITEMS[0][0].get_width() // 2, 64))
    for index, item in enumerate(OPTION_ITEMS):
        item.set_alpha(255 if index == optionChoice else 127)
        surface.blit(item, (128 + 128 * index, 128 + 270 * index))
