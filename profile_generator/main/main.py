import logging
import sys

from profile_generator import configuration, integration, log

from . import generator
from .generator import (
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
        cfg = configuration.create_from_template(cfg_template)
        for name, body in cfg.items():
            content = generator.create_profile_content(
                template, body, integration.CONFIGURATION_SCHEMA.process
            )
            _persist_profile(name, content, output_dir)
    except ConfigFileReadError:
        console_logger.error("%s: file read failure", cfg_file_name)
    except InvalidConfigFileError as exc:
        console_logger.error("%s: invalid configuration", cfg_file_name)
        logger.error(exc.errors)


def _persist_profile(name: str, content: str, output_dir: str) -> None:
    logger = log.get_console_logger()
    try:
        generator.persist_profile(name, content, output_dir)
        logger.info("Profile has been created: %s", name)
    except ProfileWriteError as exc:
        logger.error("%s: file write failure", exc.filename)
