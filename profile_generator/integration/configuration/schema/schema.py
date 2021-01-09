from configuration.schema import list_of, map_of, object_of
from feature import raw
from feature.details.sharpening import capture
from feature.tone.contrast import bezier

from ... import field_names

_CURVE_SCHEMA = object_of(**{field_names.BEZIER: bezier.SCHEMA})
_TONE_SCHEMA = object_of(**{field_names.CURVE: _CURVE_SCHEMA})

_SHARPENING_SCHEMA = object_of(**{field_names.CAPTURE_SHARPENING: capture.SCHEMA})
_DETAILS_SCHEMA = object_of(**{field_names.SHARPENING: _SHARPENING_SCHEMA})

_CONFIG_SCHEMA = object_of(
    **{
        field_names.RAW: raw.SCHEMA,
        field_names.TONE: _TONE_SCHEMA,
        field_names.DETAILS: _DETAILS_SCHEMA,
    }
)

SCHEMA = object_of(defaults=_CONFIG_SCHEMA, templates=list_of(map_of(_CONFIG_SCHEMA)))
