import math

from profile_generator.model import linalg
from profile_generator.model.color.space.color_space import ColorSpace
from profile_generator.model.linalg import Vector


def normalize(srgb: Vector) -> Vector:
    return [x / 255 for x in srgb]


def ev_comp(
    rgb: Vector,
    color_space: ColorSpace,
    compensation: float,
) -> Vector:
    if math.isclose(compensation, 0):
        return rgb

    linear = (color_space.inverse_gamma(x) for x in rgb)
    linear = (x * 2 ** compensation for x in linear)
    return [color_space.gamma(x) for x in linear]


def rgb_to_hsv(rgb: Vector) -> Vector:
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


def luminance(linear_rgb: Vector, color_space: ColorSpace) -> float:
    coeffs = color_space.xyz_matrix[1]
    return linalg.multiply_vector_vector(coeffs, linear_rgb)
