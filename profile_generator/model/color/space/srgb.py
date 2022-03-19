import math

from .. import white_point
from .color_space import ColorSpace

SRGB_XY = [[0.64, 0.33], [0.3, 0.6], [0.15, 0.06]]


def gamma(x: float) -> float:
    if x <= 0.003040:
        return 12.92310 * x
    else:
        return 1.055 * math.exp(math.log(x) / 2.4) - 0.055


def gamma_derivative(x: float) -> float:
    if x <= 0.003040:
        return 12.92310
    else:
        return 1.055 * math.exp(math.log(x) / 2.4) / x / 2.4


def inverse_gamma(x: float) -> float:
    if x <= 0.039286:
        return x / 12.92310
    else:
        return math.exp(math.log((x + 0.055) / 1.055) * 2.4)


def inverse_gamma_derivative(x: float) -> float:
    if x <= 0.039286:
        return 1 / 12.92310
    else:
        return math.exp(math.log((x + 0.055) / 1.055) * 2.4) * (
            2.4 / ((x + 0.055) / 1.055) / 1.055
        )


SRGB = ColorSpace(
    [
        [0.41245643908969243, 0.357576077643909, 0.18043748326639894],
        [0.21267285140562264, 0.715152155287818, 0.07217499330655958],
        [0.01933389558232931, 0.11919202588130297, 0.9503040785363679],
    ],
    [
        [3.240454162114103, -1.5371385127977157, -0.49853140955601577],
        [-0.9692660305051869, 1.8760108454466944, 0.041556017530349834],
        [0.05564343095911475, -0.20402591351675384, 1.057225188223179],
    ],
    white_point.D65_XYZ,
    gamma,
    inverse_gamma,
)
