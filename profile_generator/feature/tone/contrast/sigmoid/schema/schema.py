from collections.abc import Mapping
from typing import Any, Final

from profile_generator.model.view import raw_therapee
from profile_generator.schema import SchemaField, object_of, range_of

from .. import contrast_sigmoid


class Field:
    LINEAR_GREY18: Final = SchemaField("linear_grey18", 0.1)
    SLOPE: Final = SchemaField("slope", 1.6)


def _process(data: Any) -> Mapping[str, str]:
    linear_grey18 = data.get(*Field.LINEAR_GREY18)
    slope = data.get(*Field.SLOPE)
    tone_curve = contrast_sigmoid.get_tone_curve(linear_grey18, slope)
    return {
        "Curve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, tone_curve
        ),
    }


SCHEMA = object_of(
    {
        Field.LINEAR_GREY18.name: range_of(0.01, 0.75),
        Field.SLOPE.name: range_of(1.0, 4.0),
    },
    _process,
)
