import pygame
import typing

T = typing.TypeVar('T')

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
    # t => t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1,
    return a + (b - a) * ((4 * (p ** 3)) if p < .5 else (1 + (p - 1) * ((2 * p - 2) ** 2)))
