from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.color import rgb
from profile_generator.model.view import raw_therapee
from profile_generator.schema import SchemaField, object_of, range_of

from .. import contrast_sigmoid


class Field:
    GREY18: Final = SchemaField("grey18", 90.0)
    SLOPE: Final = SchemaField("slope", 1.6)


class Template:
    CURVE: Final = "Curve"


def _process(data: Any) -> Mapping[str, str]:
    grey18 = rgb.normalize_value(data.get(*Field.GREY18))
    slope = data.get(*Field.SLOPE)
    curve = contrast_sigmoid.get_tone_curve(grey18, slope)
    return {
        Template.CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, curve
        )
    }


SCHEMA = object_of(
    {
        Field.GREY18.name: range_of(16.0, 240.0),
        Field.SLOPE.name: range_of(1.0, 4.0),
    },
    _process,
)
