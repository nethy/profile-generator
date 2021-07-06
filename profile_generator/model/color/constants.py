from profile_generator.model import linalg
from profile_generator.model.linalg import Vector

from . import lab, white_point, xyz


def lab_to_luminance(lab_color: Vector) -> float:
    color = lab.to_xyz(lab_color, white_point.D50_XYZ)
    color = linalg.transform(xyz.D50_TO_D65_ADAPTATION, color)
    return color[1]


SRGB_MIDDLE_GREY_LUMINANCE = lab_to_luminance([50, 0, 0])
