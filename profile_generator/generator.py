import json
import sys
from json import JSONDecodeError
from typing import Any, Callable, Dict, List

from profile_generator.configuration.preprocessor import dot_notation
from profile_generator.configuration.schema import Schema, SchemaError
from profile_generator.util import file

_PROFILES_DIR = "profiles"

_TEMPLATES_DIR = "templates"

_RAW_THERAPEE_TEMPLATE = "raw_therapee.pp3"


class NoConfigFileError(Exception):
    pass


def get_config_files() -> List[str]:
    if len(sys.argv) < 2:
        raise NoConfigFileError

    return sys.argv[1:]


class OutputDirCreationFailure(Exception):
    pass


def create_output_dir() -> str:
    try:
        return file.create_dir(_PROFILES_DIR)
    except OSError as exc:
        raise OutputDirCreationFailure from exc


class TemplateFileReadError(Exception):
    pass


def get_profile_template() -> str:
    try:
        path = file.get_full_path(_TEMPLATES_DIR, _RAW_THERAPEE_TEMPLATE)
        return file.read_file(path)
    except OSError as exc:
        raise TemplateFileReadError from exc


class ConfigFileReadError(Exception):
    pass


class InvalidConfigFileError(Exception):
    def __init__(self, errors: List[SchemaError]):
        super().__init__()
        self.errors = errors


def load_configuration_file(file_name: str, schema: Schema) -> Dict[str, Any]:
    try:
        raw_config = file.read_file(file_name)
        cfg_template = json.loads(raw_config)
        cfg_template = dot_notation.expand(cfg_template)
        errors = schema.validate(cfg_template)
        if len(errors) > 0:
            raise InvalidConfigFileError(errors)
        return cfg_template
    except OSError as exc:
        raise ConfigFileReadError from exc
    except JSONDecodeError as exc:
        raise InvalidConfigFileError([]) from exc


class ProfileWriteError(Exception):
    pass


def generate_profile(
    name: str,
    config: Dict[str, Any],
    marshall: Callable[[Dict[str, Any]], Dict[str, str]],
    template: str,
    output_dir: str,
) -> None:
    try:
        output_filename = f"{name}.pp3"
        template_args = marshall(config)
        output = template.format(**template_args)
        file.write_file(output, output_dir, output_filename)
    except Exception as exc:
        raise ProfileWriteError from exc
