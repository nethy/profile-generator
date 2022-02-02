from profile_generator.model.color.space import SRGB

from . import lab

LUMINANCE_10_SRGB = SRGB.gamma(lab.to_xyz([10, 0, 0])[1])
LUMINANCE_15_SRGB = SRGB.gamma(lab.to_xyz([15, 0, 0])[1])
LUMINANCE_20_SRGB = SRGB.gamma(lab.to_xyz([20, 0, 0])[1])
LUMINANCE_50_SRGB = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
LUMINANCE_80_SRGB = SRGB.gamma(lab.to_xyz([80, 0, 0])[1])
LUMINANCE_85_SRGB = SRGB.gamma(lab.to_xyz([85, 0, 0])[1])
LUMINANCE_90_SRGB = SRGB.gamma(lab.to_xyz([90, 0, 0])[1])
LUMINANCE_95_SRGB = SRGB.gamma(lab.to_xyz([95, 0, 0])[1])
