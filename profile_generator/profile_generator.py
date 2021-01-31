import json
import sys
from typing import Any, Callable, Dict, List

from profile_generator.configuration.schema import Schema
from profile_generator.util import file

_PROFILES_DIR = "profiles"

_TEMPLATES_DIR = "templates"

_RAW_THERAPEE_TEMPLATE = "raw_therapee.pp3"


class OutputDirCreationFailure(Exception):
    pass


class TemplateFileReadError(Exception):
    pass


class NoConfigFileError(Exception):
    pass


class ConfigFileReadError(Exception):
    pass


class InvalidConfigFileError(Exception):
    pass


def get_config_files() -> List[str]:
    if len(sys.argv) < 2:
        raise NoConfigFileError

    return sys.argv[1:]


def create_output_dir() -> str:
    try:
        return file.create_dir(_PROFILES_DIR)
    except OSError as exc:
        raise OutputDirCreationFailure from exc


def get_profile_template() -> str:
    try:
        path = file.get_full_path(_TEMPLATES_DIR, _RAW_THERAPEE_TEMPLATE)
        return file.read_file(path)
    except OSError as exc:
        raise TemplateFileReadError from exc


def load_configuration_file(file_name: str, schema: Schema) -> Dict[str, Any]:
    try:
        raw_config = file.read_file(file_name)
    except OSError as exc:
        raise ConfigFileReadError from exc
    cfg_template = json.loads(raw_config)
    errors = schema.validate(cfg_template)
    if len(errors) > 0:
        raise InvalidConfigFileError
    return cfg_template
