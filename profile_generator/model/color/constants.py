from profile_generator.model.color.space import SRGB

from . import lab

LUMINANCE_50_SRGB = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
LUMINANCE_55_SRGB = SRGB.gamma(lab.to_xyz([55, 0, 0])[1])
LUMINANCE_60_SRGB = SRGB.gamma(lab.to_xyz([60, 0, 0])[1])
LUMINANCE_65_SRGB = SRGB.gamma(lab.to_xyz([65, 0, 0])[1])
