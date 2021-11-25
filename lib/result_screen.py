import pygame

import lib.globals
import lib.font
import lib.scene
import lib.sound

fontLargeRenderer = lib.font.FontRenderer(lib.font.FONT_LARGE, (255, 255, 255))

commentText = tuple(fontLargeRenderer.render(x) for x in (
    '满身疮痍。\n以通关为目标继续努力吧！',
    '完全通关了呢！真了不起！',
    '以No Miss的结果完美通关了！\n很不容易呢！不中弹很困难吧？',
    'No Miss No Hyper通关了！\n厉害啊……\n去尝试挑战C○VE的作品吧！',
))

def update():
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.sound.sfx['PAGE'].play()
        lib.sound.playBgm('TITLE')
        lib.globals.currentScene = lib.scene.Scene.TITLE

def draw(surface: pygame.Surface):
    surface.blit(lib.scene.BACKGROUND_RESULT, (0, 0))
    for text, (posX, posY) in (
        ((
            'Type-A 诱导攻击型',
            'Type-B 广范围型',
            'Type-C 前方集中型',
        )[lib.globals.optionType], (288, 160)),
        (str(lib.globals.score), (288, 200)),
        (str(lib.globals.grazeCount), (288, 240)),
        (str(lib.globals.missedCount), (288, 280)),
        (str(lib.globals.hyperUsedCount), (288, 320)),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
    if not lib.globals.allCleared:
        commentSurface = commentText[0]
    elif not lib.globals.missedCount:
        if not lib.globals.hyperUsedCount:
            commentSurface = commentText[3]
        else:
            commentSurface = commentText[2]
    else:
        commentSurface = commentText[1]
    surface.blit(commentSurface, (354, 148))
