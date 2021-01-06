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
        try:
            os.makedirs(path, exist_ok=True)
        except:
            logging.error("Directory create error.", exc_info=True)
            raise
    return path


def read_file(*paths: str) -> str:
    try:
        path = os.path.join(*paths)
        with open(path, "rt") as reader:
            return reader.read()
    except:
        logging.error("File open error.", exc_info=True)
        raise


def write_file(content: str, *paths: str) -> None:
    try:
        path = os.path.join(*paths)
        with open(path, "wt") as writer:
            writer.write(content)
    except:
        logging.error("File write error.", exc_info=True)
        raise
