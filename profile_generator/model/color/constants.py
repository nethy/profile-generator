from profile_generator.model.color.space import SRGB

from . import lab

LUMINANCE_15_SRGB = SRGB.gamma(lab.to_xyz([15, 0, 0])[1])
LUMINANCE_50_SRGB = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
LUMINANCE_85_SRGB = SRGB.gamma(lab.to_xyz([85, 0, 0])[1])
