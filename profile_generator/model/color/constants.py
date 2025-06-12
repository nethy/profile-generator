from profile_generator.model.color import lab
from profile_generator.model.color.space import SRGB

from . import lab

GREY18_LAB = 0.5
GREY18_LINEAR = lab.to_xyz([GREY18_LAB * 100, 0, 0])[1]
GREY18_RGB = SRGB.gamma(GREY18_LINEAR)
