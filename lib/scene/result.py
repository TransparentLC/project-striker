import pygame

import lib.constants
import lib.font
import lib.globals
import lib.replay
import lib.scene.title
import lib.sound
import lib.stg_overlay
import lib.utils

background = pygame.image.load(lib.utils.getResourceHandler('assets/ui-result-background.webp')).convert()
fontLargeRenderer = lib.font.FontRenderer(lib.font.FONT_LARGE, (255, 255, 255))

# 一行16个全角字符
commentText = tuple(fontLargeRenderer.render(x) for x in (
    '满身疮痍……\n以不续关通关为目标继续努力吧！',
    '完全通关了呢！真了不起！',
    '以No Miss的结果完美通关了！\n很不容易呢！不中弹很困难吧？',
    'No Miss No Hyper通关了！\n厉害啊……\n你真的没有使用秘籍吗？',
    '因为续关了，所以你并不能见到最终\nBOSS。\n下次再尝试以没有续关的状态攻略到\n这里吧！',
))
saveReplayText = fontLargeRenderer.render('保存本次游戏的REPLAY？\n\n\n　　　　　　　↑↓←→－输入机签\n　　　　　　　Ｚ－确认　Ｘ－放弃\n　　按住ＬＳｈｉｆｔ快速选择字符')
cannotSaveReplayText = fontLargeRenderer.render('在续关的情况下不能保存REPLAY。')
replayNameBuffer = bytearray(ord(' ') for i in range(8))
replayNameInputPosition = 0
replayNameInputPositionBlink = 0

def returnToTitle():
    lib.sound.sfx['PAGE'].play()
    lib.sound.playBgm('TITLE')
    lib.globals.nextScene = lib.scene.title

def update():
    global replayNameInputPosition
    global replayNameInputPositionBlink

    if lib.globals.continueCount:
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            returnToTitle()
    else:
        replayNameInputPositionBlink += 1
        replayNameInputPositionBlink &= 31
        if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
            lib.replay.saveReplay(replayNameBuffer)
            returnToTitle()
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            returnToTitle()
        if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
            replayNameInputPosition -= 1
            replayNameInputPosition %= 8
        if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
            replayNameInputPosition += 1
            replayNameInputPosition %= 8
        if lib.globals.keys[pygame.K_UP] and (lib.globals.keys[pygame.K_LSHIFT] or not lib.globals.keysLastFrame[pygame.K_UP]):
            replayNameBuffer[replayNameInputPosition] = lib.replay.replayNameCharsAscii[(lib.replay.replayNameCharsAscii.index(replayNameBuffer[replayNameInputPosition]) - 1) % len(lib.replay.replayNameChars)]
        if lib.globals.keys[pygame.K_DOWN] and (lib.globals.keys[pygame.K_LSHIFT] or not lib.globals.keysLastFrame[pygame.K_DOWN]):
            replayNameBuffer[replayNameInputPosition] = lib.replay.replayNameCharsAscii[(lib.replay.replayNameCharsAscii.index(replayNameBuffer[replayNameInputPosition]) + 1) % len(lib.replay.replayNameChars)]

def draw(surface: pygame.Surface):
    surface.blit(background, (0, 0))
    for text, (posX, posY) in (
        (lib.constants.OPTION_TYPE_NAME[lib.globals.optionType], (576, 280)),
        (f'Continue×{lib.globals.continueCount}' if lib.globals.continueCount else str(lib.globals.score), (576, 360)),
        (str(lib.globals.grazeCount), (576, 440)),
        (str(lib.globals.missedCount), (576, 520)),
        (str(lib.globals.hyperUsedCount), (576, 600)),
        (f'{lib.globals.phaseBonusCount} / {len(lib.constants.PHASE_NAME)}', (576, 680)),
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

    surface.blit(commentSurface, (708, 256))
    if lib.globals.continueCount:
        surface.blit(cannotSaveReplayText, (708, 418))
    else:
        surface.blit(saveReplayText, (708, 418))
        surface.blit(
            fontLargeRenderer.render('[' + ''.join(lib.replay.replayNameCharsFullWidth[x] for x in replayNameBuffer) + ']'),
            (824, 482)
        )
        surface.blit(
            fontLargeRenderer.render(''.join(('＿' if i == replayNameInputPosition and replayNameInputPositionBlink & 16 else '　') for i in range(8))),
            (834, 490)
        )
