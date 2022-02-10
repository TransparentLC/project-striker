import platform
import pygame

import lib.constants
import lib.globals
import lib.font
import lib.sound
import lib.utils

BACKGROUND = pygame.image.load(lib.utils.getResourceHandler('assets/ui-title-background.webp')).convert()
SHADE = pygame.Surface((1050, 700), pygame.SRCALPHA)
pygame.draw.rect(SHADE, (0, 0, 0, 192), SHADE.get_rect(), 0, 8)
MENU = pygame.image.load(lib.utils.getResourceHandler('assets/ui-title-menu.webp')).convert_alpha()
MENU_ITEMS = tuple(
    (
        MENU.subsurface((0, x * 64, 256, 64)),
        MENU.subsurface((256, x * 64, 256, 64)),
    )
    for x in range(5)
)

import lib.scene.config
import lib.scene.manual
import lib.scene.player_data
import lib.scene.select_option

VERSION_TEXT = tuple(lib.font.FONT_SMALL.render(x, True, (255, 255, 255)) for x in (
    (
        f'Built at {lib.constants.BUILD_INFO[1]} (Commit {lib.constants.BUILD_INFO[0][:7]}) with Python {platform.python_version()} Pygame {pygame.version.ver}'
        if lib.constants.BUILD_INFO else
        f'Built with Python {platform.python_version()} Pygame {pygame.version.ver}'
    ),
    '© 2022 TransparentLC https://akarin.dev',
))

menuChoice = 0

def update():
    global menuChoice

    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.sound.sfx['MENU'].play()
        if menuChoice == 0:
            lib.globals.nextScene = lib.scene.select_option
            lib.scene.select_option.optionChoice = 0
        elif menuChoice == 1:
            lib.globals.nextScene = lib.scene.manual
            lib.scene.manual.currentPage = 0
        elif menuChoice == 2:
            lib.globals.nextScene = lib.scene.player_data
            lib.scene.player_data.currentPage = 0
            lib.scene.player_data.currentType = 0
        elif menuChoice == 3:
            lib.globals.nextScene = lib.scene.config
            lib.scene.config.currentItem = 0
        elif menuChoice == 4:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    elif (
        (lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]) or
        (lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT])
    ):
        menuChoice = (menuChoice - 1) % len(MENU_ITEMS)
        lib.sound.sfx['MENU'].play()
    elif (
        (lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]) or
        (lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT])
    ):
        menuChoice = (menuChoice + 1) % len(MENU_ITEMS)
        lib.sound.sfx['MENU'].play()

def draw(surface: pygame.Surface):
    surface.blits((
        (BACKGROUND, (0, 0)),
        *((item[0 if menuChoice == index else 1], (512, 536 + index * 64)) for index, item in enumerate(MENU_ITEMS)),
        *((item, (640 - item.get_width() // 2, 880 + index * 24)) for index, item in enumerate(VERSION_TEXT)),
    ))
