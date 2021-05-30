from functools import partial

from profile_generator.feature import colors, raw
from profile_generator.feature.details import noise_reduction
from profile_generator.feature.details.sharpening import capture, output
from profile_generator.feature.tone.contrast import bezier, local, sigmoid
from profile_generator.profile import marshaller

from .. import field_names

_TONE_CONTRAST_LOCAL = f"{field_names.TONE}.{field_names.CONTRAST}"
_TONE_CURVE_BEZIER = f"{field_names.TONE}.{field_names.CURVE}.{field_names.BEZIER}"
_TONE_CURVE_SIGMOID = f"{field_names.TONE}.{field_names.CURVE}.{field_names.SIGMOID}"
_NOISE_REDUCTION = f"{field_names.DETAILS}.{field_names.NOISE_REDUCTION}"
_CAPTURE_SHARPENING = (
    f"{field_names.DETAILS}.{field_names.SHARPENING}.{field_names.CAPTURE_SHARPENING}"
)
_OUTPUT_SHARPENING = (
    f"{field_names.DETAILS}.{field_names.SHARPENING}.{field_names.OUTPUT_SHARPENING}"
)

marshallers = {
    field_names.RAW: raw.get_profile_args,
    _TONE_CONTRAST_LOCAL: local.get_profile_args,
    _TONE_CURVE_BEZIER: bezier.get_profile_args,
    _TONE_CURVE_SIGMOID: sigmoid.get_profile_args,
    _NOISE_REDUCTION: noise_reduction.get_profile_args,
    _CAPTURE_SHARPENING: capture.get_profile_args,
    _OUTPUT_SHARPENING: output.get_profile_args,
    field_names.COLORS: colors.get_profile_args,
}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
