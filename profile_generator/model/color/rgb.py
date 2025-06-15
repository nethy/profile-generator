import math

from profile_generator.model import linalg
from profile_generator.model.color.space.color_space import ColorSpace
from profile_generator.model.linalg import Vector
from profile_generator.util import validation


def normalize(rgb: Vector) -> Vector:
    return [normalize_value(x) for x in rgb]


def normalize_value(value: float) -> float:
    return value / 255


def to_linear_value(value: float, color_space: ColorSpace) -> float:
    validation.is_in_closed_interval(value, 0.0, 1.0)
    return color_space.inverse_gamma(value)


def from_linear_value(linear_value: float, color_space: ColorSpace) -> float:
    validation.is_in_closed_interval(linear_value, 0.0, 1.0)
    return color_space.gamma(linear_value)


def ev_comp(
    rgb: Vector,
    color_space: ColorSpace,
    compensation: float,
) -> Vector:
    if math.isclose(compensation, 0):
        return rgb

    linear = (color_space.inverse_gamma(x) for x in rgb)
    linear = (x * math.pow(2, compensation) for x in linear)
    return [color_space.gamma(x) for x in linear]


def to_hsv(rgb: Vector) -> Vector:
    max_value = max(rgb)
    min_value = min(rgb)
    delta = max_value - min_value
    hue = saturation = 0.0
    if delta > 1e-9:
        r, g, b = rgb
        if max_value == r:
            hue = (g - b) / delta
        elif max_value == g:
            hue = 2 + (b - r) / delta
        elif max_value == b:
            hue = 4 + (r - g) / delta

        hue /= 6

        if hue < 0:
            hue += 1
        elif hue > 1:
            hue -= 1

        if max_value > 1e-9:
            saturation = delta / max_value

    return [hue, saturation, max_value]


def from_hsv(hsv: Vector) -> Vector:
    h, s, v = hsv
    chroma = s * v
    hue_phase = h * 360 / 60
    secondary = chroma * (1 - abs(hue_phase % 2 - 1))
    intermediate: Vector = []
    if 0 <= hue_phase < 1:
        intermediate = [chroma, secondary, 0]
    elif 1 <= hue_phase < 2:
        intermediate = [secondary, chroma, 0]
    elif 2 <= hue_phase < 3:
        intermediate = [0, chroma, secondary]
    elif 3 <= hue_phase < 4:
        intermediate = [0, secondary, chroma]
    elif 4 <= hue_phase < 5:
        intermediate = [secondary, 0, chroma]
    elif 5 <= hue_phase < 6:
        intermediate = [chroma, 0, secondary]
    modifier = v - chroma
    return [x + modifier for x in intermediate]


def luminance(linear_rgb: Vector, color_space: ColorSpace) -> float:
    coeffs = color_space.xyz_matrix[1]
    return linalg.multiply_vector_vector(coeffs, linear_rgb)
