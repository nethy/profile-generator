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
    CURVE2: Final = "Curve2"
    AB_CURVE: Final = "ABCurve"
    COLOR_TONING_SATURATION: Final = "CTLabRegionSaturation"


def _process(data: Any) -> Mapping[str, str]:
    grey18 = rgb.normalize_value(data.get(*Field.GREY18))
    slope = data.get(*Field.SLOPE)
    flat_curve = contrast_sigmoid.get_flat(grey18)
    contrast_curve = contrast_sigmoid.get_contrast(slope)
    chromaticity_curve = contrast_sigmoid.get_chromaticity_curve(slope)
    return {
        Template.CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, flat_curve
        ),
        Template.CURVE2: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, contrast_curve
        ),
        Template.AB_CURVE: raw_therapee.present_curve(
            raw_therapee.CurveType.STANDARD, chromaticity_curve
        ),
    }


SCHEMA = object_of(
    {
        Field.GREY18.name: range_of(16.0, 240.0),
        Field.SLOPE.name: range_of(1.0, 5.0),
    },
    _process,
)
