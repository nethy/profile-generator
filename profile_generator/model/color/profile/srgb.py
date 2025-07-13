import math

from .. import illuminant
from .color_profile import ColorProfile

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


SRGB = ColorProfile(
    [
        [0.4124078805165856, 0.3575895737668074, 0.1804325976875519],
        [0.21264781339136446, 0.7151791475336148, 0.07217303907502076],
        [0.01933161939921493, 0.11919652458893577, 0.9502783478211068],
    ],
    [
        [3.2408357063031548, -1.5373195017079069, -0.4985901086620238],
        [-0.9692294485284497, 1.8759400411649523, 0.041554449125785216],
        [0.055644937617959946, -0.2040314379325196, 1.057253814741238],
    ],
    illuminant.D65_XYZ,
    gamma,
    inverse_gamma,
)
