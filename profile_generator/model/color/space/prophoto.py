import math

from .. import white_point
from .color_space import ColorSpace

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


PROPHOTO = ColorSpace(
    [
        [0.4560993669437902, 0.3787102635615131, 0.12941036949469678],
        [0.16469737586795635, 0.7835384763341651, 0.05176414779787871],
        [0.0, 0.14364872066126358, 0.6815612793387364],
    ],
    [
        [2.6233934787916144, -1.1932679794417997, -0.40748473804080276],
        [-0.559215782890511, 1.548646195588611, -0.011438486457898737],
        [0.11786266946348113, -0.3263991830185436, 1.4696303242428785],
    ],
    white_point.D50_XYZ,
    gamma,
    inverse_gamma,
)
