from collections.abc import Callable, Mapping

from .profile_params import ProfileParams

ProfileGenerator = Callable[[ProfileParams], Mapping[str, str]]
