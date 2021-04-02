import logging
import sys

from profile_generator import configuration, generator, integration, log
from profile_generator.configuration.preprocessor import dot_notation
from profile_generator.generator import (
    ConfigFileReadError,
    InvalidConfigFileError,
    NoConfigFileError,
    OutputDirCreationFailure,
    ProfileWriteError,
    TemplateFileReadError,
)


def main() -> None:
    log.init()
    console_logger = log.get_console_logger()

    try:
        output_dir = generator.create_output_dir()
        template = generator.get_profile_template()
        for cfg_file_name in generator.get_config_files():
            logging.info("processing configuration file: %s", cfg_file_name)
            process_config_file(cfg_file_name, template, output_dir)
    except NoConfigFileError:
        console_logger.error("No config file provided.")
        sys.exit(1)
    except OutputDirCreationFailure:
        console_logger.error("Target directory creation failure", exc_info=True)
        sys.exit(1)
    except TemplateFileReadError:
        console_logger.error("Template file read failure", exc_info=True)
        sys.exit(1)


def process_config_file(cfg_file_name: str, template: str, output_dir: str) -> None:
    logger = logging.getLogger(__name__)
    console_logger = log.get_console_logger()
    try:
        cfg_template = generator.load_configuration_file(
            cfg_file_name, integration.SCHEMA
        )
        config = configuration.create_from_template(cfg_template, dot_notation.expand)
        for name, body in config.items():
            logging.info("creating profile: %s", name)
            generator.generate_profile(
                name, body, integration.get_profile_args, template, output_dir
            )
            console_logger.info("Profile has been created: %s", name)
    except ConfigFileReadError:
        console_logger.error("%s: file read failure", cfg_file_name)
    except InvalidConfigFileError as exc:
        console_logger.error("%s: invalid configuration", cfg_file_name)
        logger.error(exc.errors)
    except ProfileWriteError:
        console_logger.error("%s: file write failure", cfg_file_name)
