import math

from profile_generator.model.linalg import Vector


def normalize(srgb: Vector) -> Vector:
    return [x / 255 for x in srgb]


def ev_comp_srgb(srgb: Vector, compensation: float) -> Vector:
    if math.isclose(compensation, 0):
        return srgb
    linear = map(srgb_gamma_inverse, srgb)
    linear = map(lambda x: x * 2 ** compensation, linear)
    return list(map(srgb_gamma, linear))


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


def srgb_luminance(rgb: Vector) -> float:
    return (
        0.21267285140562264 * rgb[0]
        + 0.715152155287818 * rgb[1]
        + 0.07217499330655958 * rgb[2]
    )


def srgb_gamma(x: float) -> float:
    if x <= 0.0031308:
        return max(0.0, 12.92 * x)
    else:
        return min(1.0, 1.055 * x ** (1 / 2.4) - 0.055)


def srgb_gamma_inverse(x: float) -> float:
    if x <= 0.040449936:
        return max(0.0, x / 12.92)
    else:
        return min(1.0, ((x + 0.055) / 1.055) ** 2.4)


def prophoto_gamma(x: float) -> float:
    if x < 0.001953125:
        return max(0.0, 16 * x)
    else:
        return min(1.0, x ** (1 / 1.8))


def prophoto_gamma_inverse(x: float) -> float:
    if x < 0.03125:
        return max(0.0, x / 16)
    else:
        return min(1.0, x ** 1.8)
