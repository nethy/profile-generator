from collections.abc import Sequence
from typing import Final, Optional

from profile_generator.unit import DECIMALS, Point

_EQ_STRENGTH = 0.25
_ONE_SIDE_EQ_STRENGTH = 0.5


class CurveType:
    LINEAR: Final = "0;"
    STANDARD: Final = "1;"
    CONTROL_CAGE: Final = "3;"
    FLEXIBLE: Final = "4;"


class WbSetting:
    CAMERA: Final = "Camera"
    CUSTOM: Final = "Custom"


class EqPoint(Point):
    def present(self) -> str:
        return self._present(_EQ_STRENGTH, _EQ_STRENGTH)

    def _present(self, left: float, right: float) -> str:
        return (
            f"{self.x:.{DECIMALS}f};{self.y:.{DECIMALS}f};"
            + f"{left:.{DECIMALS}f};{right:.{DECIMALS}f};"
        )


class LinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(0, 0)


class LeftLinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(0, _ONE_SIDE_EQ_STRENGTH)


class RightLinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(_ONE_SIDE_EQ_STRENGTH, 0)


def present_curve(curve_type: str, points: Sequence[Point]) -> str:
    if len(points) == 0:
        return CurveType.LINEAR
    return curve_type + "".join((_present_point(p) for p in points))


def _present_point(point: Point) -> str:
    return f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"


def present_equalizer(points: Optional[Sequence[EqPoint]]) -> str:
    if points is None or len(points) == 0:
        return CurveType.LINEAR
    return CurveType.STANDARD + "".join(p.present() for p in points)
