import typing

def clamp(value: typing.Union[int, float], min: typing.Union[int, float], max: typing.Union[int, float]) -> typing.Union[int, float]:
    if value < min:
        return min
    elif max < value:
        return max
    else:
        return value

def frameToSeconds(frame: int) -> str:
    return f'{frame / 60:.02f}'

def linearInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * p

def easeInQuadInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * (p ** 2)

def easeOutQuadInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * (p * (2 - p))

def easeInOutQuadInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * ((2 * (p ** 2)) if p < .5 else (-1 + (4 - 2 * p) * p))

def easeInCubicInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * (p ** 3)

def easeOutCubicInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    return a + (b - a) * ((p - 1) ** 3 + 1)

def easeInOutCubicInterpolation(p: float, a: typing.Union[int, float], b: typing.Union[int, float]) -> float:
    # t => t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1,
    return a + (b - a) * ((4 * (p ** 3)) if p < .5 else (1 + (p - 1) * ((2 * p - 2) ** 2)))
