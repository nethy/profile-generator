import math

from .. import illuminant
from .color_profile import ColorProfile

PROPHOTO_XY = [[0.7347, 0.2653], [0.29, 0.6], [0.15, 0.06]]


def gamma(x: float) -> float:
    if x < 0.001953125:
        return max(0.0, 16 * x)
    else:
        return min(1.0, math.pow(x, 1 / 1.8))


def inverse_gamma(x: float) -> float:
    if x < 0.03125:
        return max(0.0, x / 16)
    else:
        return min(1.0, math.pow(x, 1.8))


PROPHOTO = ColorProfile(
    [
        [0.4560938239426135, 0.37871205305773753, 0.12940611742084848],
        [0.164695374291514, 0.7835421787401466, 0.05176244696833939],
        [0.0, 0.14364939943569355, 0.6815388850831354],
    ],
    [
        [2.623425361427109, -1.193282481470696, -0.4074896902858538],
        [-0.5592131404751877, 1.5486388779009441, -0.01143843240858036],
        [0.11786654223846664, -0.3264099079630662, 1.4696786138971307],
    ],
    illuminant.D50_XYZ,
    gamma,
    inverse_gamma,
)
