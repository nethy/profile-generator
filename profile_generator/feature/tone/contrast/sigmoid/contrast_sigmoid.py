from profile_generator.model.sigmoid import (
    contrast_gradient,
    find_contrast_gradient,
    find_curve_brightness,
    get_curve,
    get_curve_with_hl_protection,
)
from profile_generator.unit import Point, Strength, equals

MAX_CONTRAST = 16


def calculate(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
    sample_size: int = 17,
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    curve = get_curve(contrast, brightness)
    return [
        Point(x, curve(x) * (offsets[1] - offsets[0]) + offsets[0])
        for x in (i / (sample_size - 1) for i in range(sample_size))
    ]


def calculate_with_hl_protection(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
    sample_size: int = 17,
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    curve = get_curve_with_hl_protection(contrast, brightness)
    return [
        Point(x, curve(x) * (offsets[1] - offsets[0]) + offsets[0])
        for x in (i / (sample_size - 1) for i in range(sample_size))
    ]


def _corrigate_contrast(c: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    if equals(1, highlight - shadow):
        return c
    gradient = contrast_gradient(c) / (highlight - shadow)
    return find_contrast_gradient(gradient)
