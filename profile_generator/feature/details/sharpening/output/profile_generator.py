from collections.abc import Mapping

from profile_generator.main.profile_params import ProfileParams


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    output_sharpening = profile_params.details.sharpening.output
    if exclude_default and not output_sharpening.is_set:
        return {}

    enabled = output_sharpening.enabled.value
    threshold = output_sharpening.threshold.value
    radius = output_sharpening.radius.value
    amount = output_sharpening.amount.value
    damping = output_sharpening.damping.value
    iterations = output_sharpening.iterations.value

    return {
        "SharpeningEnabled": str(enabled).lower(),
        "SharpeningContrast": str(threshold),
        "DeconvRadius": f"{radius:.2f}",
        "DeconvAmount": str(amount),
        "DeconvDamping": str(damping),
        "DeconvIterations": str(iterations),
    }
