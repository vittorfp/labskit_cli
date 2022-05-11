"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import os
import shutil
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
    fetch_template, append_requirement,
    mark_notebooks_as_readonly,
    clean_readonly_folder, enable_files_overwrite
)
from .operations import BashUtils, EnvironmentManagerOperations, RCManager
from .registry import Template
from .settings import SettingsManager
from ..constants import DEFAULT_ENV, INIT, VENV, CONDA, REMOTE_INDEX, LOCAL_TEMPLATE

logger = logging.getLogger('gryphon')


def init(template: Template, location, python_version, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()
    with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
        data = json.load(f)
        env_type = data.get("environment_management", DEFAULT_ENV)

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    project_home = Path.cwd() / location
    os.makedirs(project_home, exist_ok=True)

    if template.registry_type == REMOTE_INDEX:

        template_folder = fetch_template(template, project_home)

        try:
            enable_files_overwrite(
                source_folder=template_folder / "notebooks",
                destination_folder=project_home / "notebooks"
            )
            mark_notebooks_as_readonly(template_folder / "notebooks")

            # Move files to destination
            shutil.copytree(
                src=Path(template_folder),
                dst=project_home,
                dirs_exist_ok=True
            )
        finally:
            clean_readonly_folder(template_folder)

    elif template.registry_type == LOCAL_TEMPLATE:

        BashUtils.copy_project_template(
            template_destiny=project_home,
            template_source=Path(template.path)
        )
    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")

    # RC file
    rc_file = RCManager.get_rc_file(Path.cwd() / location)
    RCManager.log_operation(template, performed_action=INIT, logfile=rc_file)
    RCManager.log_new_files(template, performed_action=INIT, logfile=rc_file)

    # Git
    repo = init_new_git_repo(folder=project_home)
    initial_git_commit(repo)

    # Requirements
    for r in template.dependencies:
        append_requirement(r, location)

    RCManager.log_add_library(template.dependencies, logfile=rc_file)

    # ENV Manager
    if env_type == VENV:
        # VENV
        EnvironmentManagerOperations.create_venv(folder=location, python_version=python_version)
        EnvironmentManagerOperations.install_libraries_venv(folder=project_home)
        EnvironmentManagerOperations.install_extra_nbextensions_venv(folder_path=project_home)
        EnvironmentManagerOperations.change_shell_folder_and_activate_venv(project_home)
    elif env_type == CONDA:
        # CONDA
        EnvironmentManagerOperations.create_conda_env(project_home, python_version=python_version)
        EnvironmentManagerOperations.install_libraries_conda(project_home)
        EnvironmentManagerOperations.install_extra_nbextensions_conda(project_home)
        EnvironmentManagerOperations.change_shell_folder_and_activate_conda_env(project_home)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")
