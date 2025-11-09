import bisect
from collections.abc import Callable, Mapping
from operator import itemgetter
from typing import TypeAlias

from profile_generator.main.profile_params import (
    ColorToning,
    ColorToningChannel,
    ProfileParams,
)
from profile_generator.model import interpolation, linalg
from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Vector, curve

ColorTone: TypeAlias = tuple[float, Vector]


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    toning_params = profile_params.colors.grading.toning
    if exclude_default and not toning_params.is_set:
        return {}

    is_enabled = any(
        map(
            lambda param: param.as_list() != [0, 0, 0],
            (
                toning_params.black,
                toning_params.shadow,
                toning_params.midtone,
                toning_params.highlight,
                toning_params.white,
            ),
        )
    )

    if is_enabled:
        toning_curve = get_rgb_toning(toning_params)
        reds, greens, blues = curve.as_points_multiple(toning_curve)
    else:
        reds = greens = blues = []

    return {
        "RGBCurvesEnabled": str(is_enabled).lower(),
        "RGBCurvesRCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, reds
        ),
        "RGBCurvesGCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, greens
        ),
        "RGBCurvesBCurve": raw_therapee.present_curve(
            raw_therapee.CurveType.FLEXIBLE, blues
        ),
    }


def get_rgb_toning(
    color_toning: ColorToning,
) -> Callable[[float], Vector]:
    lab_mapping = get_lab_toning(color_toning)
    return _as_rgb(lab_mapping)


def get_lab_toning(color_toning: ColorToning) -> Callable[[float], Vector]:
    tones = _get_tones(color_toning)

    def lab_curve(x: float) -> Vector:
        i = bisect.bisect(tones, x, key=itemgetter(0))
        if i == 0:
            return tones[0][1]
        elif i == len(tones):
            return linalg.add_vectors(tones[-1][1], [100, 0, 0])
        else:
            return _interpolate(x, tones[i - 1], tones[i])

    if len(tones) > 0:
        return lab_curve
    else:
        return lambda x: [x, 0, 0]


def _as_rgb(lab_toning: Callable[[float], Vector]) -> Callable[[float], Vector]:
    def rgb_toning(x: float) -> Vector:
        luminance = lab.from_xyz_luminance(rgb.to_linear_value(x))
        lab_color = lab_toning(luminance)
        return rgb.from_linear(
            rgb.clip_linear(xyz.to_linear_rgb(lab.to_xyz(lab_color)))
        )

    return rgb_toning


def _get_tones(color_toning: ColorToning) -> list[ColorTone]:
    channel = color_toning.channels.value
    if channel == ColorToningChannel.ONE:
        return [
            _to_lab(0.0, color_toning.black.as_list()),
            _to_lab(50.0, color_toning.midtone.as_list()),
            _to_lab(100.0, color_toning.white.as_list()),
        ]
    elif channel == ColorToningChannel.TWO:
        return [
            _to_lab(0.0, color_toning.black.as_list()),
            _to_lab(100 * 1 / 3, color_toning.shadow.as_list()),
            _to_lab(100 * 2 / 3, color_toning.highlight.as_list()),
            _to_lab(100.0, color_toning.white.as_list()),
        ]
    elif channel == ColorToningChannel.THREE:
        return [
            _to_lab(0.0, color_toning.black.as_list()),
            _to_lab(25.0, color_toning.shadow.as_list()),
            _to_lab(50.0, color_toning.midtone.as_list()),
            _to_lab(75.0, color_toning.highlight.as_list()),
            _to_lab(100.0, color_toning.white.as_list()),
        ]
    else:
        raise ValueError(f"Unhandled value: {channel}")


def _to_lab(luminance: float, lch_tone: Vector) -> ColorTone:
    return (luminance, lab.from_lch(lch_tone))


def _interpolate(x: float, left: ColorTone, right: ColorTone) -> Vector:
    return [
        x
        + interpolation.interpolate_values(
            left[1][0],
            right[1][0],
            interpolation.hermite,
            x,
            left[0],
            right[0],
        ),
        interpolation.interpolate_values(
            left[1][1], right[1][1], interpolation.hermite, x, left[0], right[0]
        ),
        interpolation.interpolate_values(
            left[1][2], right[1][2], interpolation.hermite, x, left[0], right[0]
        ),
    ]
