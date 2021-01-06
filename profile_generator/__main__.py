import json
import logging
import sys
from json import JSONDecodeError

import configuration
import integration
import log
from util import file

_PROFILES_DIR = "profiles"

_TEMPLATES_DIR = "templates"

_RAW_THERAPEE_TEMPLATE = "raw_therapee.pp3"


def main() -> None:
    log.init()
    console_logger = log.get_console_logger()

    if len(sys.argv) < 2:
        console_logger.error("No config file provided.")
        sys.exit(1)

    try:
        output_dir = file.create_dir(_PROFILES_DIR)
    except OSError:
        console_logger.error("target directory creation failure", exc_info=True)
        sys.exit(1)

    try:
        template = file.read_file(_TEMPLATES_DIR, _RAW_THERAPEE_TEMPLATE)
    except OSError:
        console_logger.error("template file read failure", exc_info=True)
        sys.exit(1)

    for cfg_file_name in sys.argv[1:]:
        logging.info("processing configuration file: %s", cfg_file_name)
        try:
            raw_config = file.read_file(cfg_file_name)
        except OSError:
            console_logger.error("%s: file read failure", cfg_file_name, exc_info=True)

        try:
            try_generate_profiles(cfg_file_name, raw_config, template, output_dir)
        except (JSONDecodeError, TypeError):
            console_logger.error(
                "%s: invalid json format", cfg_file_name, exc_info=True
            )
        except OSError:
            console_logger.error("%s: file write failure", cfg_file_name, exc_info=True)


def try_generate_profiles(
    file_name: str, raw_config: str, template: str, output_dir: str
) -> None:
    console_logger = log.get_console_logger()
    cfg_template = json.loads(raw_config)
    errors = integration.SCHEMA.validate(cfg_template)
    if len(errors) > 0:
        console_logger.error("%s: invalid configuration schema", file_name)
    cfg = configuration.create_from_template(cfg_template)
    for name, body in cfg.items():
        logging.info("creating profile: %s", name)
        output_filename = f"{name}.pp3"
        template_args = integration.get_profile_args(body)
        output = template.format(**template_args)
        file.write_file(output, output_dir, output_filename)
        console_logger.info("Profile has been created: %s", name)


if __name__ == "__main__":
    main()
