import concurrent.futures
import logging
import os
import sys
from collections.abc import Callable, Mapping
from typing import Any

from profile_generator import configuration, generator, integration, log
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
        cfg = configuration.create_from_template(cfg_template)
        with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as thread_pool:
            creators = [
                thread_pool.submit(
                    _create_profile_content,
                    name,
                    template,
                    body,
                    integration.CONFIGURATION_SCHEMA.process,
                    console_logger,
                )
                for name, body in cfg.items()
            ]
            for creator in concurrent.futures.as_completed(creators):
                _persist_profile(*creator.result(), output_dir, console_logger)
    except ConfigFileReadError:
        console_logger.error("%s: file read failure", cfg_file_name)
    except InvalidConfigFileError as exc:
        console_logger.error("%s: invalid configuration", cfg_file_name)
        logger.error(exc.errors)


def _create_profile_content(
    name: str,
    template: str,
    cfg: Mapping[str, Any],
    marshall: Callable[[Any], Mapping[str, str]],
    logger: logging.Logger,
) -> tuple[str, str]:
    logger.info("Creating profile: %s", name)
    return generator.create_profile_content(name, template, cfg, marshall)


def _persist_profile(
    name: str, content: str, output_dir: str, logger: logging.Logger
) -> None:
    try:
        generator.persist_profile(name, content, output_dir)
        logger.info("Profile has been created: %s", name)
    except ProfileWriteError as exc:
        logger.error("%s: file write failure", exc.filename)
