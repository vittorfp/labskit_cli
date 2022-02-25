"""
Module containing the code for the init command in the CLI.
"""
import os
import json
import logging
from pathlib import Path
from ..constants import DEFAULT_ENV, CONFIG_FILE, INIT, VENV, CONDA
from .common_operations import (
    install_libraries_venv,
    copy_project_template,
    create_venv,
    init_new_git_repo,
    initial_git_commit,
    log_operation, log_new_files,
    change_shell_folder_and_activate_venv,
    get_rc_file,
    create_conda_env, install_libraries_conda,
    install_extra_nbextensions_venv,
    install_extra_nbextensions_conda
)


logger = logging.getLogger('gryphon')


def init(template, location, python_version, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    # Files
    copy_project_template(
        template_destiny=Path(location),
        template_source=Path(template.path)
    )

    # RC file
    rc_file = get_rc_file(Path.cwd() / location)
    log_operation(template, performed_action=INIT, logfile=rc_file)
    log_new_files(template, performed_action=INIT, logfile=rc_file)

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    # ENV Manager
    if env_type == VENV:
        # VENV
        create_venv(folder=location, python_version=python_version)
        install_libraries_venv(folder=location)
        install_extra_nbextensions_venv(location)
        change_shell_folder_and_activate_venv(location)
    elif env_type == CONDA:
        # CONDA
        create_conda_env(location, python_version=python_version)
        install_libraries_conda(location)
        install_extra_nbextensions_conda(location)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")
