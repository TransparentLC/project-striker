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
    for x in range(4)
)

import lib.scene.config
import lib.scene.manual
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
        if menuChoice == 0:
            lib.globals.nextScene = lib.scene.select_option
            lib.scene.select_option.optionChoice = 0
            lib.sound.sfx['MENU'].play()
        elif menuChoice == 1:
            lib.globals.nextScene = lib.scene.manual
            lib.scene.manual.currentPage = 0
            lib.sound.sfx['MENU'].play()
        elif menuChoice == 2:
            lib.globals.nextScene = lib.scene.config
            lib.scene.manual.currentItem = 0
            lib.sound.sfx['MENU'].play()
        elif menuChoice == 3:
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
    surface.blit(BACKGROUND, (0, 0))
    for index, item in enumerate(MENU_ITEMS):
        surface.blit(item[0 if menuChoice == index else 1], (512, 600 + index * 64))
    for index, item in enumerate(VERSION_TEXT):
        surface.blit(item, (640 - item.get_width() // 2, 880 + index * 24))
