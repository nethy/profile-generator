import math

from .. import white_point
from .color_space import ColorSpace

SRGB_XY = [[0.64, 0.33], [0.3, 0.6], [0.15, 0.06]]

_A = 0.055
_G = 2.4

_X = _A / (_G - 1)
_PHI = (math.pow(1 + _A, _G) * math.pow(_G - 1, _G - 1)) / (
    math.pow(_A, _G - 1) * math.pow(_G, _G)
)

_X_PHI = _X / _PHI


def gamma(x: float) -> float:
    if x <= _X_PHI:
        return max(0.0, _PHI * x)
    else:
        return min(1.0, (1 + _A) * math.pow(x, 1 / _G) - _A)


def gamma_derivative(x: float) -> float:
    if x <= _X_PHI:
        return _PHI
    else:
        return (1 + _A) / _G * math.pow(x, 1 / _G - 1)


def inverse_gamma(x: float) -> float:
    if x <= _X:
        return max(0.0, x / _PHI)
    else:
        return min(1.0, math.pow((x + _A) / (1 + _A), _G))


def inverse_gamma_derivative(x: float) -> float:
    if x <= _X:
        return 1 / _PHI
    else:
        return _G * math.pow((x + _A) / (1 + _A), _G - 1) / (1 + _A)


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
