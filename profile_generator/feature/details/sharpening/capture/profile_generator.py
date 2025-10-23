from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    capture_sharpening = profile_params.details.sharpening.capture
    radius = capture_sharpening.radius.value
    if radius < 0.4:
        radius = 0.0
    threshold = capture_sharpening.threshold.value
    return {
        "PDSEnabled": str(radius > 0.0).lower(),
        "PDSDeconvRadius": str(round(radius, 2)),
        "PDSContrast": str(threshold),
    }
