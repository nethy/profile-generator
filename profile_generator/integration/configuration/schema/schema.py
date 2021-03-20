from profile_generator.configuration.schema import list_of, map_of, object_of
from profile_generator.feature import raw
from profile_generator.feature.details import noise_reduction
from profile_generator.feature.details.sharpening import capture, output
from profile_generator.feature.tone.contrast import bezier, local

from ... import field_names

_CURVE_SCHEMA = object_of(**{field_names.BEZIER: bezier.SCHEMA})
_TONE_SCHEMA = object_of(
    **{field_names.CURVE: _CURVE_SCHEMA, field_names.CONTRAST: local.SCHEMA}
)

_SHARPENING_SCHEMA = object_of(
    **{
        field_names.CAPTURE_SHARPENING: capture.SCHEMA,
        field_names.OUTPUT_SHARPENGING: output.SCHEMA,
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
    }
)

SCHEMA = object_of(defaults=_CONFIG_SCHEMA, templates=list_of(map_of(_CONFIG_SCHEMA)))
