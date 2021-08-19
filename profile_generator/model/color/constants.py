from profile_generator.model.color.space import SRGB

from . import lab

MIDDLE_GREY_LUMINANCE_SRGB = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
