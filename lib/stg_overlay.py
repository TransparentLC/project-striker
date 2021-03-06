import enum
import pygame

import lib.constants
import lib.font
import lib.native_utils
import lib.globals
import lib.utils

overlay = pygame.image.load(lib.utils.getResourceHandler('assets/overlay.webp')).convert_alpha()
overlayPhaseBonus = overlay.subsurface((0, 0, 512, 48))
overlayPhaseBonusFailed = overlay.subsurface((0, 48, 512, 48))
overlayLifeExtend = overlay.subsurface((0, 96, 256, 48))
overlayHyperExtend = overlay.subsurface((256, 96, 256, 48))
overlayAllClear = overlay.subsurface((0, 144, 320, 80))
overlayContinue = overlay.subsurface((0, 224, 320, 80))
overlayWarning = lib.native_utils.xbrzScale(2, overlay.subsurface((0, 304, 320, 128)))
overlayNumber = (
    *(overlay.subsurface((320 + 24 * x, 144, 24, 32)) for x in range(5)),
    *(overlay.subsurface((320 + 24 * x, 176, 24, 32)) for x in range(5)),
)
overlayNumber2x = tuple(lib.native_utils.xbrzScale(2, x) for x in overlayNumber)
overlayNumberSmall = tuple(overlay.subsurface((320 + 12 * x, 208, 12, 16)) for x in range(10))
overlayPhaseName = tuple(lib.utils.renderOutlinedText(lib.font.FONT_NORMAL, x, (255, 255, 255), (0, 0, 0), 3, 18) for x in lib.constants.PHASE_NAME)
overlayPhaseName2x = tuple(lib.native_utils.xbrzScale(2, x) for x in overlayPhaseName)
overlayPhaseBonusText = overlay.subsurface((448, 144, 64, 20))
overlayPhaseHistoryText = overlay.subsurface((448, 164, 64, 20))
overlayPhaseBonusFailedText = overlay.subsurface((448, 184, 52, 20))
overlayPhaseHistoryDivide = overlay.subsurface((500, 184, 12, 20))

class OverLayStatusIndex(enum.IntEnum):
    LIFE_REMAIN = 0
    HYPER_REMAIN = 1
    CLEAR_REMAIN = 2
    WARNING_REMAIN = 3
    PHASE_BONUS_REMAIN = 4
    PHASE_NAME_REMAIN = 5
    PHASE_BONUS_VALUE = 6

overlayStatus = [0, 0, 0, 0, 0, 0, 0, 0]

def update():
    for i in range(6):
        if overlayStatus[i] > 0:
            overlayStatus[i] -= 1

def draw(surface: pygame.Surface):
    if lib.globals.replayRecording and lib.globals.continueRemain:
        continueRemainSurface = lib.utils.renderBitmapNumber(lib.globals.continueRemain // 60, overlayNumber2x)
        surface.blits((
            (overlayContinue, (224, 320)),
            (continueRemainSurface, (384 - continueRemainSurface.get_width() // 2, 576 - continueRemainSurface.get_height())),
        ))

    blitSeq = []
    for img, remain, centerX, centerY in (
        (overlayHyperExtend, overlayStatus[OverLayStatusIndex.HYPER_REMAIN], 384, 96),
        (overlayLifeExtend, overlayStatus[OverLayStatusIndex.LIFE_REMAIN], 384, 96),
        (
            overlayPhaseBonus if overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE] else overlayPhaseBonusFailed,
            overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN], 384, 192
        ),
        (overlayAllClear, overlayStatus[OverLayStatusIndex.CLEAR_REMAIN], 384, 192),
    ):
        if not remain:
            continue
        if remain < 30:
            img = pygame.transform.scale(
                img,
                (
                    img.get_width(),
                    int(lib.utils.linearInterpolation(remain / 30, 0, img.get_height()))
                )
            )
        elif remain > 210:
            img = pygame.transform.scale(
                img, (
                    img.get_width(),
                    int(lib.utils.easeOutQuadInterpolation(1 - (remain - 210) / 30, 0, img.get_height()))
                )
            )
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
        blitSeq.append((overlayWarning, (384 - overlayWarning.get_width() // 2, 320 - overlayWarning.get_height() // 2)))

    if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] and overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE]:
        phaseBonusDigits = lib.utils.splitDigits(overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE])
        phaseBonusSurface = pygame.Surface((24 * len(phaseBonusDigits), 64), pygame.SRCALPHA)
        blitSeqInner = []
        for i, x in enumerate(phaseBonusDigits):
            appearTime = 240 - overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN]
            imgDigit = overlayNumber[x].copy()
            imgDigit.set_alpha(lib.utils.clamp((appearTime - 3 * i) / 30 * 255, 0, 255))
            imgX = 24 * i
            imgY = lib.utils.clamp((appearTime - 9 * i) ** 2 / 16, 0, 16)
            blitSeqInner.append((imgDigit, (imgX, imgY)))
        phaseBonusSurface.blits(blitSeqInner)
        if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] < 30:
            phaseBonusSurface = pygame.transform.scale(
                phaseBonusSurface,
                (
                    phaseBonusSurface.get_width(),
                    int(lib.utils.linearInterpolation(
                        overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] / 30,
                        0, phaseBonusSurface.get_height()
                    ))
                )
            )
        blitSeq.append((phaseBonusSurface, (384 - phaseBonusSurface.get_width() // 2, 288 - phaseBonusSurface.get_height() // 2)))

    if lib.globals.phaseIndex:
        if overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] > 60:
            interpolationP = 1 - (overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] - 60) / 60
            phaseNameSurface = overlayPhaseName2x[lib.globals.phaseIndex - 1]
            phaseNameSurface = pygame.transform.scale(
                phaseNameSurface,
                tuple(
                    round(x * lib.utils.easeOutCubicInterpolation(interpolationP, 1, .5))
                    for x in phaseNameSurface.get_size()
                )
            )
            phaseNameSurface.set_alpha(round(lib.utils.easeOutCubicInterpolation(interpolationP, 0, 255)))
            surface.blit(
                phaseNameSurface,
                (lib.utils.easeOutCubicInterpolation(interpolationP, 384, 752) - phaseNameSurface.get_width(), 768)
            )
        else:
            interpolationP = 1 - overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] / 60
            phaseNameSurface = overlayPhaseName[lib.globals.phaseIndex - 1]
            surface.blit(
                phaseNameSurface,
                (752 - phaseNameSurface.get_width(), lib.utils.easeInOutCubicInterpolation(interpolationP, 768, 16))
            )
        if overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] < 30:
            bonusText = lib.utils.renderBitmapNumber(lib.globals.phaseBonus, overlayNumberSmall) if lib.globals.phaseBonus else overlayPhaseBonusFailedText
            historyText = lib.utils.renderBitmapNumber(
                lib.globals.savedata[lib.globals.optionType]['phaseHistory'][lib.globals.phaseIndex - 1]['bonus'],
                overlayNumberSmall,
            )
            alpha = round(lib.utils.linearInterpolation(
                overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] / 30,
                255, 0
            ))
            for b in (
                (overlayPhaseBonusText, (450, 54)),
                (bonusText, (600 - bonusText.get_width(), 56 if lib.globals.phaseBonus else 54)),
                (overlayPhaseHistoryText, (605, 54)),
                (historyText, (705 - historyText.get_width(), 56)),
                (overlayPhaseHistoryDivide, (705, 54)),
                (
                    lib.utils.renderBitmapNumber(
                        lib.globals.savedata[lib.globals.optionType]['phaseHistory'][lib.globals.phaseIndex - 1]['total'],
                        overlayNumberSmall,
                    ),
                    (715, 56),
                ),
            ):
                b[0].set_alpha(alpha)
                blitSeq.append(b)
    surface.blits(blitSeq)
