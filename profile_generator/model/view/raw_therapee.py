from collections.abc import Callable, Iterable
from typing import TypeVar

from profile_generator.model.equalizer import EqPoint
from profile_generator.unit import DECIMALS, Point

_T = TypeVar("_T")
_Presenter = Callable[[_T], str]


class CurveType:
    LINEAR = "0;"
    STANDARD = "1;"
    FLEXIBLE = "4;"


class WbSetting:
    CAMERA = "Camera"
    CUSTOM = "Custom"


def _present_point(point: Point) -> str:
    return f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"


def present_curve(points: Iterable[Point]) -> str:
    return "".join((_present_point(p) for p in points))


def _present_eq_point(point: EqPoint) -> str:
    return (
        f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"
        + f"{point.left:.{DECIMALS}f};{point.right:.{DECIMALS}f};"
    )


def present_equalizer(points: Iterable[EqPoint]) -> str:
    return _present(_present_eq_point, points)


def _present(presenter: _Presenter, items: Iterable[_T]) -> str:
    return "".join((presenter(i) for i in items))
