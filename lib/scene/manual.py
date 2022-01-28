import os
import platform
import pygame

import lib.constants
import lib.font
import lib.scene.title
import lib.sound
import lib.globals
import lib.utils

from .title import BACKGROUND
from .title import MENU_ITEMS
from .title import SHADE

fontNormalRenderer = lib.font.FontRenderer(lib.font.FONT_NORMAL, (255, 255, 255))

# 一行42个全角字符，一页最多17行，用----------------分页
with lib.utils.getResourceHandler('scriptfiles/manual.txt') as f:
    manualPages = tuple(fontNormalRenderer.render(x.strip()) for x in (f.read().decode('utf-8') + f'''
----------------
# 关于

源代码以GNU AGPL 3.0许可证发布。
https://github.com/TransparentLC/project-striker

Commit: {lib.constants.BUILD_INFO[0] if lib.constants.BUILD_INFO else None}
Build time: {lib.constants.BUILD_INFO[1] if lib.constants.BUILD_INFO else None}
Mod loaded: {os.environ.get('STRIKER_MODDED_RESOURCE') if lib.utils.MODDED_RESOURCE_HANDLER else None}

Built with:
　Python {platform.python_version()}
　Pygame {pygame.version.ver}
''').split('----------------'))

currentPage = 0

def update():
    global currentPage
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        currentPage -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        currentPage += 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()
    currentPage %= len(manualPages)

def draw(surface: pygame.Surface):
    surface.blit(BACKGROUND, (0, 0))
    surface.blit(MENU_ITEMS[1][0], (640 - MENU_ITEMS[1][0].get_width() // 2, 64))
    surface.blit(SHADE, (115, 184))
    surface.blit(manualPages[currentPage], (135, 198))
