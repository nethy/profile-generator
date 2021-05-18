import logging
import math
from collections.abc import Sequence

from profile_generator.model import bezier
from profile_generator.model.bezier import WeightedPoints
from profile_generator.unit import Line, Point, Strength

_logger = logging.getLogger(__name__)

_BLACK_POINT = Point(0, 0)
_WHITE_POINT = Point(1, 1)

_SHADOW_PROTECTION_SLOPE = 0.13165249758739585347152645740972  # 7.5 degree
_HIGHLIGHT_PROTECTION_SLOPE = 0.26794919243112270647255365849413  # 15 degree

_POINTS_COUNT = 8

_CONTRAST_LIMIT = 4


def calculate(
    grey: Point,
    strength: Strength,
    weights: tuple[float, float],
) -> Sequence[Point]:
    _logger.info("Calculating contrast curve: {grey} {strength}")
    (shadow, highlight) = _get_control_points(grey, strength)
    toe = _get_bezier_curve(
        [(_BLACK_POINT, weights[0]), (shadow, weights[0]), (grey, 1)]
    )
    shoulder = _get_bezier_curve(
        [(grey, 1), (highlight, weights[1]), (_WHITE_POINT, weights[1])]
    )
    return toe + shoulder[1:]


def _get_control_points(grey: Point, strength: Strength) -> tuple[Point, Point]:
    contrast_correction = math.sqrt(grey.y / grey.x)
    q = (1 - 1 / (strength.value * (_CONTRAST_LIMIT - 1) + 1)) / contrast_correction
    contrast_line = _get_contrast_line(grey, q)
    shadow_line = Line(-_SHADOW_PROTECTION_SLOPE, 0 + _SHADOW_PROTECTION_SLOPE * grey.x)
    shadow = contrast_line.intersect(shadow_line)
    highlight_line = Line(
        -_HIGHLIGHT_PROTECTION_SLOPE, 1 + _HIGHLIGHT_PROTECTION_SLOPE * grey.x
    )
    highlight = contrast_line.intersect(highlight_line)
    return (shadow, highlight)


def _get_contrast_line(grey: Point, q: float) -> Line:
    gradient = grey.y / (grey.x * (1 - q))
    offset = grey.y - gradient * grey.x
    return Line(gradient, offset)


def _get_bezier_curve(points: WeightedPoints) -> list[Point]:
    return [
        bezier.get_point_at(points, 1 / (_POINTS_COUNT - 1) * i)
        for i in range(_POINTS_COUNT)
    ]
