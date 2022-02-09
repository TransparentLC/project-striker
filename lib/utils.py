import math
import os
import pygame
import tarfile
import typing

T = typing.TypeVar('T')

PACKED_RESOURCE_HANDLER = tarfile.open('resources.tar', 'r:') if os.path.exists('resources.tar') else None
MODDED_RESOURCE_HANDLER = tarfile.open(os.environ.get('STRIKER_MODDED_RESOURCE'), 'r:') if os.environ.get('STRIKER_MODDED_RESOURCE') is not None and os.path.exists(os.environ.get('STRIKER_MODDED_RESOURCE')) else None

def clamp(value: T, min: T, max: T) -> T:
    if value < min:
        return min
    elif max < value:
        return max
    else:
        return value

def frameToSeconds(frame: int) -> str:
    return f'{frame / 60:.02f}'

def splitDigits(value: int) -> typing.Sequence[int]:
    if not value:
        return [0]
    result = []
    while value:
        result.append(value % 10)
        value //= 10
    result.reverse()
    return result

def renderBitmapNumber(value: int, bitmapDigits: typing.Sequence[pygame.Surface]) -> pygame.Surface:
    digits = splitDigits(value)
    width = bitmapDigits[0].get_width()
    result = pygame.Surface((width * len(digits), bitmapDigits[0].get_height()), pygame.SRCALPHA)
    result.blits((bitmapDigits[x], (width * i, 0)) for i, x in enumerate(digits))
    return result

outlineOffsetCache: dict[tuple[int, int], set[tuple[int, int]]] = dict()

def renderOutlinedText(font: pygame.font.Font, text: str, color: pygame.Color, outlineColor: pygame.Color, outlineWidth: int, divide: int = None) -> pygame.Surface:
    outlineSurface = font.render(text, True, outlineColor)
    resultSurface = pygame.Surface(tuple(x + 2 * outlineWidth for x in outlineSurface.get_size()), pygame.SRCALPHA)
    if divide is None:
        divide = outlineWidth * 4
    offsetCacheKey = (divide, outlineWidth)
    if offsetCacheKey not in outlineOffsetCache:
        outlineOffsetCache[offsetCacheKey] = set()
        for r in range(1, outlineWidth + 1):
            outlineOffsetCache[offsetCacheKey].update(
                (
                    round(outlineWidth + r * math.cos(i / divide * 2 * math.pi)),
                    round(outlineWidth + r * math.sin(i / divide * 2 * math.pi)),
                )
                for i in range(divide)
            )
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [(outlineSurface, x) for x in outlineOffsetCache[offsetCacheKey]]
    blitSequence.append((font.render(text, True, color), (outlineWidth, outlineWidth)))
    resultSurface.blits(blitSequence)
    return resultSurface

def getResourceHandler(path: str) -> typing.IO[bytes]:
    if MODDED_RESOURCE_HANDLER and path in MODDED_RESOURCE_HANDLER.getnames():
        return MODDED_RESOURCE_HANDLER.extractfile(path)
    elif PACKED_RESOURCE_HANDLER and path in PACKED_RESOURCE_HANDLER.getnames():
        return PACKED_RESOURCE_HANDLER.extractfile(path)
    else:
        return open(path, 'rb')

def linearInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * p

def easeInQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p ** 2)

def easeOutQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p * (2 - p))

def easeInOutQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((2 * (p ** 2)) if p < .5 else (-1 + (4 - 2 * p) * p))

def easeInCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p ** 3)

def easeOutCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((p - 1) ** 3 + 1)

def easeInOutCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((4 * (p ** 3)) if p < .5 else (1 + (p - 1) * ((2 * p - 2) ** 2)))
