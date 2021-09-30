from profile_generator.feature import camera, colors, raw
from profile_generator.feature.details import noise_reduction
from profile_generator.feature.details.sharpening import capture, output
from profile_generator.feature.tone.contrast import local, sigmoid
from profile_generator.schema import list_of, map_of, object_of, type_of

_CURVE_SCHEMA = object_of({"sigmoid": sigmoid.SCHEMA})
_TONE_SCHEMA = object_of({"curve": _CURVE_SCHEMA, "contrast": local.SCHEMA})

_SHARPENING_SCHEMA = object_of(
    {
        "capture": capture.SCHEMA,
        "output": output.SCHEMA,
    }
)
_DETAILS_SCHEMA = object_of(
    {
        "sharpening": _SHARPENING_SCHEMA,
        "noise_reduction": noise_reduction.SCHEMA,
    }
)

CONFIGURATION_SCHEMA = object_of(
    {
        "camera": camera.SCHEMA,
        "raw": raw.SCHEMA,
        "tone": _TONE_SCHEMA,
        "details": _DETAILS_SCHEMA,
        "colors": colors.SCHEMA,
    }
)

_TEMPLATE_SCHAME = object_of(
    {
        "optional": type_of(bool),
        "directory": type_of(bool),
        "settings": map_of(CONFIGURATION_SCHEMA),
    }
)

SCHEMA = object_of(
    {"defaults": CONFIGURATION_SCHEMA, "templates": list_of(_TEMPLATE_SCHAME)}
)
