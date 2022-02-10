"""
Gryphon interactive wizard.
"""
import logging
import os
import shutil
import traceback
import json
import platform
import argparse
from .core.registry import RegistryCollection
from .wizard import init, generate, add, about, exit_program, settings
from .wizard.wizard_text import Text
from .wizard.questions import CommonQuestions
from .constants import (
    INIT, GENERATE, ADD, ABOUT, QUIT, BACK, SETTINGS,
    GRYPHON_HOME, DEFAULT_CONFIG_FILE, CONFIG_FILE, DATA_PATH
)
from .logger import logger


def output_error(er: Exception):
    logger.debug("Traceback (most recent call last):")
    for line in traceback.format_tb(er.__traceback__):
        logger.debug(line)

    # sample:                    ValueError(er)
    logger.error(f'{er.__class__.__name__}({er}). Please report to the support.')


if platform.system() == "Windows":
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from colorama import init
    init()

try:
    with open(CONFIG_FILE, "r") as f:
        settings_file = json.load(f)

except FileNotFoundError:
    os.makedirs(GRYPHON_HOME)
    shutil.copy(
        src=DEFAULT_CONFIG_FILE,
        dst=CONFIG_FILE
    )
    with open(CONFIG_FILE, "r") as f:
        settings_file = json.load(f)

try:
    # loads registry of templates to memory
    registry = RegistryCollection.from_config_file(
        settings=settings_file,
        data_path=DATA_PATH / "template_registry"
    )
except Exception as e:
    logger.error(f'Registry loading error.')
    output_error(e)
    exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    debug = parser.parse_args().debug
    if debug:
        logger.warning("Starting Gryphon in debug mode.")
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info(Text.welcome)

    while True:
        chosen_command = CommonQuestions.main_question()

        function = {
            INIT: init,
            GENERATE: generate,
            ADD: add,
            ABOUT: about,
            SETTINGS: settings,
            QUIT: exit_program
        }[chosen_command]

        try:
            response = function(DATA_PATH, registry)

            if response != BACK:
                if chosen_command in [GENERATE, ADD]:
                    logger.info("\n\n")
                    continue
                break

        except RuntimeError as er:
            logger.error(f'Runtime error: {er}')
            exit(1)

        except KeyboardInterrupt:
            logger.warning(f'Operation cancelled by user')
            exit(0)

        except Exception as er:
            output_error(er)
            exit(1)


def did_you_mean_gryphon():
    logger.info("Did you mean \"gryphon\"?")

# DONE: Figure out if the user is in a folder with .venv (and inform the user)
# DONE: Activate a verbose level of log when with this mode activated.
# TODO: Test installation.
# DONE: Create .labskitrc and populate it accordingly
# DONE: Developer documentations
# DONE: Handle errors from the pip commands

# TODO: Power user configurations
    # TODO: Whether to install gryphon inside the .venv created for projects or not


# TODO: Have a single readme file with all the readmes from other templates
# TODO: Find a way to install wexpect for windows and pexpect for linux
# TODO: Implement gitflow guidelines
# DONE: CLI fix case when more parameters are sent
# DONE: use conda
# TODO: implement test for the conda environments
# Done: Fix codec issue


if __name__ == '__main__':
    main()
