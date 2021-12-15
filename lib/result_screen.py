import pygame

import lib.globals
import lib.font
import lib.scene
import lib.sound

fontLargeRenderer = lib.font.FontRenderer(lib.font.FONT_LARGE, (255, 255, 255))

# 一行16个全角字符
commentText = tuple(fontLargeRenderer.render(x) for x in (
    '满身疮痍……\n以不续关通关为目标继续努力吧！',
    '完全通关了呢！真了不起！',
    '以No Miss的结果完美通关了！\n很不容易呢！不中弹很困难吧？',
    'No Miss No Hyper通关了！\n厉害啊……\n你真的没有使用秘籍吗？',
    '因为续关了，所以你并不能见到最终\nBOSS。\n下次再尝试以没有续关的状态攻略到\n这里吧！',
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
        )[lib.globals.optionType], (576, 320)),
        (f'Continue×{lib.globals.continueCount}' if lib.globals.continueCount else str(lib.globals.score), (576, 400)),
        (str(lib.globals.grazeCount), (576, 480)),
        (str(lib.globals.missedCount), (576, 560)),
        (str(lib.globals.hyperUsedCount), (576, 640)),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
    if not lib.globals.allCleared:
        commentSurface = commentText[0]
    elif lib.globals.continueCount:
        commentSurface = commentText[4]
    elif not lib.globals.missedCount:
        if not lib.globals.hyperUsedCount:
            commentSurface = commentText[3]
        else:
            commentSurface = commentText[2]
    else:
        commentSurface = commentText[1]
    surface.blit(commentSurface, (708, 296))
