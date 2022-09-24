import math
from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.color import rgb
from profile_generator.model.view import raw_therapee
from profile_generator.schema import SchemaField, object_of, range_of
from profile_generator.unit import Line, Point

from .. import contrast_sigmoid


class Field:
    GREY18: Final = SchemaField("grey18", 90.0)
    SLOPE: Final = SchemaField("slope", 1.6)


class Template:
    CURVE: Final = "Curve"
    A_CURVE: Final = "ACurve"
    B_CURVE: Final = "BCurve"


def _process(data: Any) -> Mapping[str, str]:
    grey18 = rgb.normalize_value(data.get(*Field.GREY18))
    slope = data.get(*Field.SLOPE)
    curve = contrast_sigmoid.get_tone_curve(grey18, slope)
    saturation_line = Line.at_point(Point(0.5, 0.5), math.pow(slope, 0.25))
    color_points = [
        Point(0, 0),
        Point(saturation_line.get_x(0), 0),
        Point(saturation_line.get_x(1), 1),
        Point(1, 1),
    ]
    return {
        Template.CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, curve
        ),
        Template.A_CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.CONTROL_CAGE,
            color_points,
        ),
        Template.B_CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.CONTROL_CAGE,
            color_points,
        ),
    }


SCHEMA = object_of(
    {
        Field.GREY18.name: range_of(16.0, 240.0),
        Field.SLOPE.name: range_of(1.0, 5.0),
    },
    _process,
)
