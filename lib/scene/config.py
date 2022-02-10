import pygame

import lib.font
import lib.scene.title
import lib.sound
import lib.globals

from .title import BACKGROUND
from .title import MENU_ITEMS
from .title import SHADE

fontLargeRenderer = lib.font.FontRenderer(lib.font.FONT_LARGE, (255, 255, 255))
fontSmallRenderer = lib.font.FontRenderer(lib.font.FONT_SMALL, (255, 255, 255))

configItems = (
    ('窗口模式', '以窗口模式运行游戏，下次启动游戏时生效。', 'windowed', bool),
    ('BGM', '控制是否播放BGM。', 'bgm', bool),
    ('Scale2x', '使用Scale2x算法对游戏画面进行放大，以平滑风格代替像素风格。', 'scale2x', bool),
    ('输入显示', '在右下角显示按下的按键。', 'inputDisplay', bool),
)
configItemSurfaces = tuple((fontLargeRenderer.render(x[0]), fontSmallRenderer.render(x[1])) for x in configItems)
arrowSurface = fontLargeRenderer.render('▶')
boolSurface = (fontLargeRenderer.render('ＯＦＦ'), fontLargeRenderer.render('Ｏ　Ｎ'))
currentItem = 0

def update():
    global currentItem
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentItem -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentItem += 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if configItems[currentItem][3] == bool:
            lib.globals.config[configItems[currentItem][2]] = not lib.globals.config[configItems[currentItem][2]]
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        if lib.globals.config['bgm']:
            if not pygame.mixer.music.get_busy():
                lib.sound.playBgm('TITLE')
        else:
            pygame.mixer.music.stop()
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()
    currentItem %= len(configItems)

def draw(surface: pygame.Surface):
    surface.blit(BACKGROUND, (0, 0))
    surface.blit(MENU_ITEMS[3][0], (640 - MENU_ITEMS[3][0].get_width() // 2, 64))
    surface.blit(SHADE, (115, 184))
    surface.blit(arrowSurface, (135, 198 + 96 * currentItem))
    for index, item in enumerate(configItems):
        surface.blit(configItemSurfaces[index][0], (183, 198 + 96 * index))
        surface.blit(configItemSurfaces[index][1], (183, 246 + 96 * index))
        if item[3] == bool:
            surface.blit(boolSurface[1 if lib.globals.config[item[2]] else 0], (1035, 198 + 96 * index))
