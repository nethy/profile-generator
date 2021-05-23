import logging
import os.path

_logger = logging.getLogger(__name__)

_ROOT = os.path.dirname(__file__)
while not _ROOT.endswith("profile_generator"):
    _ROOT = os.path.dirname(_ROOT)
_ROOT = os.path.dirname(_ROOT)

join = os.path.join


def get_full_path(*paths: str) -> str:
    return os.path.join(_ROOT, *paths)


def create_dir(*paths: str) -> str:
    path = os.path.join(*paths)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def read_file(*paths: str) -> str:
    path = os.path.join(*paths)
    with open(path, "rt") as reader:
        return reader.read()


def write_file(content: str, *paths: str) -> None:
    path = os.path.join(*paths)
    path = os.path.normpath(path)
    create_dir(os.path.dirname(path))
    with open(path, "wt") as writer:
        writer.write(content)
