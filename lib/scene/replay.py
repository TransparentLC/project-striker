import io
import pygame
import time

import lib.constants
import lib.font
import lib.globals
import lib.newgame
import lib.replay
import lib.scene.title
import lib.sound
import lib.utils

from .title import BACKGROUND
from .title import MENU_ITEMS
from .title import SHADE

fontNormalRenderer = lib.font.FontRenderer(lib.font.FONT_NORMAL, (255, 255, 255))
arrowSurface = fontNormalRenderer.render('▶')
emptySurface = fontNormalRenderer.render('还没有保存过的REPLAY。')
incorrectVersionSurface = lib.font.FONT_NORMAL.render('REPLAY版本和主程序对应版本不同，可能无法正常播放。', True, (255, 255, 0))
incorrectChecksumSurface = lib.font.FONT_NORMAL.render('REPLAY校验失败，无法播放。', True, (255, 0, 0))

replayPathList: list[str] = None
currentPage = 0
currentPageReplayData: list[tuple[str, tuple[bytes, int, int, bytes, bytes, int, int, int, int, int, int]]] = None
currentItem = 0
currentHint: pygame.Surface = None
totalPage = 0

def turnPage():
    global currentPage
    global currentPageReplayData
    if totalPage:
        currentPage %= totalPage
    currentPageReplayData = tuple((x, lib.replay.parseReplay(x)) for x in replayPathList[(currentPage * 10):(currentPage * 10 + 10)])

def update():
    global currentPage
    global currentItem
    global currentHint
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentItem = currentItem + 1
        if currentItem > min(len(currentPageReplayData) - 1, 9):
            currentPage += 1
            turnPage()
            currentItem = 0
        currentHint = None if currentPageReplayData[currentItem][1][1] == lib.replay.REPLAY_VERSION else incorrectVersionSurface
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentItem = currentItem - 1
        if currentItem < 0:
            currentPage -= 1
            turnPage()
            currentItem = len(currentPageReplayData) - 1
        currentHint = None if currentPageReplayData[currentItem][1][1] == lib.replay.REPLAY_VERSION else incorrectVersionSurface
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if lib.replay.loadReplay(currentPageReplayData[currentItem][0]):
            lib.newgame.init()
        else:
            currentHint = incorrectChecksumSurface
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()

def draw(surface: pygame.Surface):
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [
        (BACKGROUND, (0, 0)),
        (MENU_ITEMS[1][0], (640 - MENU_ITEMS[2][0].get_width() // 2, 64)),
        (SHADE, (115, 184)),
    ]

    if len(currentPageReplayData):
        blitSequence.append((arrowSurface, (135, 198 + 36 * currentItem)))
        for index, (replayPath, replayHeader) in enumerate(currentPageReplayData):
            blitSequence.append((
                fontNormalRenderer.render(f'No.{index + currentPage * 10 + 1:02d}'),
                (175, 198 + 36 * index)
            ))
            blitSequence.append((
                fontNormalRenderer.render(''.join(lib.replay.replayNameCharsFullWidth[x] for x in replayHeader[3])),
                (275, 198 + 36 * index)
            ))
            blitSequence.append((
                fontNormalRenderer.render(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(replayHeader[2]))),
                (555, 198 + 36 * index)
            ))
            blitSequence.append((
                fontNormalRenderer.render(lib.constants.OPTION_TYPE_NAME[replayHeader[6]]),
                (875, 198 + 36 * index)
            ))
        currentReplayHeader = currentPageReplayData[currentItem][1]
        blitSequence.append((
            fontNormalRenderer.render('\n'.join((
                f'机签：{"".join(lib.replay.replayNameCharsFullWidth[x] for x in currentReplayHeader[3])}',
                f'分数：{currentReplayHeader[5]}',
                '',
                f'录制时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(currentReplayHeader[2]))}',
            ))),
            (220, 660)
        ))
        blitSequence.append((
            fontNormalRenderer.render('\n'.join((
                f'自机类型：{lib.constants.OPTION_TYPE_NAME[currentReplayHeader[6]]}',
                f'MISS次数：{currentReplayHeader[7]}',
                f'火力强化次数：{currentReplayHeader[8]}',
                f'完美击破奖励次数：{currentReplayHeader[9]} / {len(lib.constants.PHASE_NAME)}',
            ))),
            (700, 660)
        ))
        if currentHint:
            blitSequence.append((currentHint, (640 - currentHint.get_width() // 2, 840 - currentHint.get_height() // 2)))
    else:
        blitSequence.append((emptySurface, (640 - emptySurface.get_width() // 2, 534 - emptySurface.get_height() // 2)))
    surface.blits(blitSequence)

    if len(currentPageReplayData):
        pygame.draw.line(surface, (255, 255, 255), (136, 574), (1144, 574))
