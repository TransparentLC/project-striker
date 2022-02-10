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

currentPage = 0
currentType = 0
totalPage = -(-len(lib.constants.PHASE_NAME) // 16)

def update():
    global currentPage
    global currentType
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        currentType -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        currentType += 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentPage = (currentPage + 1) % totalPage
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentPage = (currentPage - 1) % totalPage
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()
    currentType %= len(lib.constants.OPTION_TYPE_NAME)

def draw(surface: pygame.Surface):
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [
        (BACKGROUND, (0, 0)),
        (MENU_ITEMS[2][0], (640 - MENU_ITEMS[2][0].get_width() // 2, 64)),
        (SHADE, (115, 184)),
        (lib.font.FONT_LARGE.render(lib.constants.OPTION_TYPE_NAME[currentType], True, (255, 255, 255)), (135, 210)),
    ]

    d = lib.globals.savedata[currentType]
    s = lib.font.FONT_SMALL.render(
        f'最高分数：{d["highScore"]}',
        True,
        (255, 255, 255),
    )
    blitSequence.append((s, (1145 - s.get_width(), 210)))
    s = lib.font.FONT_SMALL.render(
        f'获得过的完美奖励：{len(tuple(x for x in d["phaseHistory"] if x["bonus"]))} / {len(lib.constants.PHASE_NAME)}',
        True,
        (255, 255, 255),
    )
    blitSequence.append((s, (1145 - s.get_width(), 234)))

    for i in range(min(16, len(lib.constants.PHASE_NAME) - currentPage * 16)):
        phaseIndex = i + currentPage * 16
        blitSequence.append((
            lib.font.FONT_NORMAL.render(f'No.{phaseIndex + 1:02d}', True, (255, 255, 255)),
            (135, 274 + 36 * i),
        ))
        d = lib.globals.savedata[currentType]["phaseHistory"][phaseIndex]
        s = lib.font.FONT_NORMAL.render(
            f'{d["bonus"]} / {d["total"]}' if d['total'] else '??? / ???',
            True,
            (255, 255, 255),
        )
        blitSequence.append((s, (1145 - s.get_width(), 274 + 36 * i)))
        blitSequence.append((
            lib.font.FONT_NORMAL.render(
                lib.constants.PHASE_NAME[phaseIndex] if d['total'] else '???',
                True,
                (255, 255, 255)
            ),
            (235, 274 + 36 * i),
        ))

    surface.blits(blitSequence)
