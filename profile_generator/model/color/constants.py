from profile_generator.model.color.space import SRGB

from . import lab

SRGB_MIDDLE_GREY_LUMINANCE = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
