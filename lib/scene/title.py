import platform
import pygame

import lib.constants
import lib.globals
import lib.font
import lib.script_engine.stage
import lib.sound
import lib.sprite.option
import lib.stg_overlay

background = pygame.image.load('assets/ui-title-background.webp').convert()

import lib.scene.stg
import lib.scene.manual

MENU = pygame.image.load('assets/ui-title-menu.webp').convert_alpha()
MENU_ITEMS = tuple(
    (
        MENU.subsurface((0, x * 64, 256, 64)),
        MENU.subsurface((256, x * 64, 256, 64)),
    )
    for x in range(3)
)

OPTION = pygame.image.load('assets/ui-title-select.webp').convert_alpha()
OPTION_ITEMS = tuple(OPTION.subsurface((0, x * 256, 768, 256)) for x in range(3))

with open('build-info.txt', 'r', encoding='utf-8') as f:
    BUILD_INFO = f.read().splitlines()

fontSmallRenderer = lib.font.FontRenderer(lib.font.FONT_SMALL, (255, 255, 255))
versionText = fontSmallRenderer.render('\n'.join((
    f'Built at {BUILD_INFO[1]} (Commit {BUILD_INFO[0][:7]})',
    f'with Python {platform.python_version()} Pygame {pygame.version.ver}',
    '© 2021 TransparentLC https://akarin.dev',
)))

def update():
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if lib.globals.menuChoice == 0:
            lib.globals.groupPlayer.sprite.position.update(192, 400)
            lib.globals.groupPlayer.sprite.invincibleRemain = 0
            lib.globals.groupPlayer.sprite.hyperRemain = 0
            lib.globals.groupPlayer.sprite.deathWait = 0
            lib.globals.score = 0
            lib.globals.scoreLastFrame = 0
            lib.globals.grazeCount = 0
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
            ):
                for s in g:
                    s.kill()
            lib.globals.menuSubChoice %= 3
            lib.globals.optionType = lib.globals.menuSubChoice
            #
            if lib.globals.menuSubChoice == 0:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
                ]
            elif lib.globals.menuSubChoice == 1:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(-15, 20), pygame.Vector2(-25, 0), 12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(15, 20), pygame.Vector2(25, 0), -12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(-30, 5), pygame.Vector2(-45, 0), 30, 0),
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(30, 5), pygame.Vector2(45, 0), -30, 0),
                ]
            elif lib.globals.menuSubChoice == 2:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeC(8, pygame.Vector2(-25, 0), pygame.Vector2(-10, -15), 0, 0),
                    lib.sprite.option.OptionTypeC(8, pygame.Vector2(25, 0), pygame.Vector2(10, -15), 0, 0),
                ]
            with open('scriptfiles/stage/stage1.txt', 'r', encoding='utf-8') as f:
                lib.globals.stageEngine = lib.script_engine.stage.Engine(f.read())
            lib.globals.nextScene = lib.scene.stg
        elif lib.globals.menuChoice == 1:
            lib.globals.nextScene = lib.scene.manual
            lib.sound.sfx['MENU'].play()
        elif lib.globals.menuChoice == 2:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        lib.globals.menuChoice = (lib.globals.menuChoice - 1) % len(MENU_ITEMS)
        lib.globals.menuSubChoice = 0
        lib.sound.sfx['MENU'].play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        lib.globals.menuChoice = (lib.globals.menuChoice + 1) % len(MENU_ITEMS)
        lib.globals.menuSubChoice = 0
        lib.sound.sfx['MENU'].play()
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        lib.globals.menuSubChoice -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        lib.globals.menuSubChoice += 1
        lib.sound.sfx['PAGE'].play()

def draw(surface: pygame.Surface):
    surface.blit(background, (0, 0))
    for index, item in enumerate(MENU_ITEMS):
        surface.blit(item[0 if lib.globals.menuChoice == index else 1], (64, 640 + index * 64))

    if lib.globals.menuChoice == 0:
        surface.blit(OPTION_ITEMS[lib.globals.menuSubChoice % 3], (400, 620))

    surface.blit(versionText, (20, 870))
