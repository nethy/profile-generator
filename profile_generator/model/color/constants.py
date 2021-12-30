from profile_generator.model.color.space import SRGB

from . import lab

LUMINANCE_25_SRGB = SRGB.gamma(lab.to_xyz([25, 0, 0])[1])
LUMINANCE_50_SRGB = SRGB.gamma(lab.to_xyz([50, 0, 0])[1])
