import enum
import pygame

import lib.globals
import lib.utils

overlay = pygame.image.load('assets/overlay.webp')
overlayPhaseBonus = overlay.subsurface((0, 0, 512, 48))
overlayLifeExtend = overlay.subsurface((0, 48, 256, 48))
overlayHyperExtend = overlay.subsurface((256, 48, 256, 48))
overlayAllClear = overlay.subsurface((0, 96, 320, 80))
overlayContinue = overlay.subsurface((0, 176, 320, 80))
overlayWarning = overlay.subsurface((0, 256, 320, 128))
overlayNumber = (
    *(overlay.subsurface((320 + 24 * x, 96, 24, 32)) for x in range(5)),
    *(overlay.subsurface((320 + 24 * x, 128, 24, 32)) for x in range(5)),
)
overlayNumber2x = tuple(pygame.transform.scale2x(x) for x in overlayNumber)

class OverLayStatusIndex(enum.IntEnum):
    LIFE_REMAIN = 0
    HYPER_REMAIN = 1
    CLEAR_REMAIN = 2
    WARNING_REMAIN = 3
    PHASE_BONUS_REMAIN = 4
    PHASE_BONUS_VALUE = 5

overlayStatus = [0, 0, 0, 0, 0, 0]

def update():
    for i in range(5):
        if overlayStatus[i] > 0:
            overlayStatus[i] -= 1

def draw(surface: pygame.Surface):
    if lib.globals.continueRemain:
        continueRemainSurface = lib.utils.renderBitmapNumber(lib.globals.continueRemain // 60, overlayNumber2x)
        surface.blits((
            (overlayContinue, (224, 320)),
            (continueRemainSurface, (384 - continueRemainSurface.get_width() // 2, 576 - continueRemainSurface.get_height())),
        ))

    blitSeq = []
    for img, remain, centerX, centerY in (
        (overlayHyperExtend, overlayStatus[OverLayStatusIndex.HYPER_REMAIN], 384, 96),
        (overlayLifeExtend, overlayStatus[OverLayStatusIndex.LIFE_REMAIN], 384, 96),
        (overlayPhaseBonus, overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN], 384, 192),
        (overlayAllClear, overlayStatus[OverLayStatusIndex.CLEAR_REMAIN], 384, 192),
    ):
        if not remain:
            continue
        if remain < 30:
            img = pygame.transform.scale(img, (img.get_width(), int(lib.utils.linearInterpolation(remain / 30, 0, img.get_height()))))
        elif remain > 210:
            img = pygame.transform.scale(img, (img.get_width(), int(lib.utils.easeOutQuadInterpolation(1 - (remain - 210) / 30, 0, img.get_height()))))
        blitSeq.append((img, (centerX - img.get_width() // 2, centerY - img.get_height() // 2)))
    if overlayStatus[OverLayStatusIndex.WARNING_REMAIN]:
        appearTime = 330 - overlayStatus[OverLayStatusIndex.WARNING_REMAIN]
        if appearTime < 60:
            appearTime %= 20
            overlayWarning.set_alpha(abs(appearTime - 10) / 10 * 255)
        elif appearTime > 300:
            overlayWarning.set_alpha((330 - appearTime) / 30 * 255)
        else:
            overlayWarning.set_alpha(255)
        blitSeq.append((overlayWarning, (384 - img.get_width() // 2, 240 - img.get_height() // 2)))
    surface.blits(blitSeq)

    if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN]:
        phaseBonusDigits = lib.utils.splitDigits(overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE])
        phaseBonusSurface = pygame.Surface((24 * len(phaseBonusDigits), 64), pygame.SRCALPHA)
        blitSeq = []
        for i, x in enumerate(phaseBonusDigits):
            appearTime = 240 - overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN]
            imgDigit = overlayNumber[x].copy()
            imgDigit.set_alpha(lib.utils.clamp((appearTime - 3 * i) / 30 * 255, 0, 255))
            imgX = 24 * i
            imgY = lib.utils.clamp((appearTime - 9 * i) ** 2 / 16, 0, 16)
            blitSeq.append((imgDigit, (imgX, imgY)))
        phaseBonusSurface.blits(blitSeq)
        if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] < 30:
            phaseBonusSurface = pygame.transform.scale(phaseBonusSurface, (phaseBonusSurface.get_width(), int(lib.utils.linearInterpolation(overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] / 30, 0, phaseBonusSurface.get_height()))))
        surface.blit(phaseBonusSurface, (384 - phaseBonusSurface.get_width() // 2, 288 - phaseBonusSurface.get_height() // 2))
