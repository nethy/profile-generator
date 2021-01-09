from configuration.schema import list_of, map_of, object_of
from feature.tone import contrast

from ... import field_names

_CONTRAST_SCHEMA = object_of(**{field_names.BEZIER: contrast.BEZIER_SCHEMA})
_TONE_SCHEMA = object_of(**{field_names.CONTRAST: _CONTRAST_SCHEMA})
_CONFIG_SCHEMA = object_of(**{field_names.TONE: _TONE_SCHEMA})

SCHEMA = object_of(defaults=_CONFIG_SCHEMA, templates=list_of(map_of(_CONFIG_SCHEMA)))
