from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.color.profile import SRGB

from . import lab

GREY18_LAB = 50
GREY18_LINEAR = lab.to_xyz([GREY18_LAB, 0, 0])[1]
GREY18_SRGB = rgb.luminance(xyz.to_rgb(lab.to_xyz([GREY18_LAB, 0, 0]), SRGB), SRGB)
