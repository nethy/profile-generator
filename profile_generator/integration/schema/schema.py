from profile_generator.feature import colors, raw
from profile_generator.feature.details import noise_reduction
from profile_generator.feature.details.sharpening import capture, output
from profile_generator.feature.tone.contrast import bezier, local, sigmoid
from profile_generator.schema import list_of, map_of, object_of, type_of

from .. import field_names

_CURVE_SCHEMA = object_of(
    **{field_names.BEZIER: bezier.SCHEMA, field_names.SIGMOID: sigmoid.SCHEMA}
)
_TONE_SCHEMA = object_of(
    **{field_names.CURVE: _CURVE_SCHEMA, field_names.CONTRAST: local.SCHEMA}
)

_SHARPENING_SCHEMA = object_of(
    **{
        field_names.CAPTURE_SHARPENING: capture.SCHEMA,
        field_names.OUTPUT_SHARPENING: output.SCHEMA,
    }
)
_DETAILS_SCHEMA = object_of(
    **{
        field_names.SHARPENING: _SHARPENING_SCHEMA,
        field_names.NOISE_REDUCTION: noise_reduction.SCHEMA,
    }
)

_CONFIG_SCHEMA = object_of(
    **{
        field_names.RAW: raw.SCHEMA,
        field_names.TONE: _TONE_SCHEMA,
        field_names.DETAILS: _DETAILS_SCHEMA,
        field_names.COLORS: colors.SCHEMA,
    }
)

_TEMPLATE_SCHAME = object_of(
    optional=type_of(bool), directory=type_of(bool), settings=map_of(_CONFIG_SCHEMA)
)

SCHEMA = object_of(defaults=_CONFIG_SCHEMA, templates=list_of(_TEMPLATE_SCHAME))
