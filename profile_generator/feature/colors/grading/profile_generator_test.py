from .matte import profile_generator_test as matte_test
from .toning import profile_generator_test as toning_test

DEFAULT = {
    **matte_test.DEFAULT,
    **toning_test.DEFAULT,
}
