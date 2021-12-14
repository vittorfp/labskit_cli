import pytest
from .utils import TEST_FOLDER
from gryphon_commands.registry import \
    RegistryCollection, GitRegistry, \
    LocalRegistry, TemplateRegistry


TEST_REPO = "https://github.com/vittorfp/template_registry.git"


def test_template_registry_1():
    registry_path = TEST_FOLDER / "data" / "ok_registry"
    registry = TemplateRegistry(templates_path=registry_path)

    metadata = registry.get_templates()
    assert "init" in metadata
    assert "generate" in metadata
    assert "sample_init" in metadata["init"]
    assert "sample_generate" in metadata["generate"]


def test_template_registry_2(capsys):
    registry_path = TEST_FOLDER / "data" / "no_metadata_registry"

    registry = TemplateRegistry(templates_path=registry_path)
    registry.get_templates()

    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "does not contain a metadata.json file." in captured.out


def test_template_registry_3(capsys):
    registry_path = TEST_FOLDER / "data" / "wrong_json_registry"

    registry = TemplateRegistry(templates_path=registry_path)
    registry.get_templates()

    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "has a malformed json on metadata.json file" in captured.out


def test_template_registry_4():
    registry_path = TEST_FOLDER / "data" / "ok_registry"

    registry = TemplateRegistry(templates_path=registry_path)

    with pytest.raises(NotImplementedError):
        registry.update_registry()


def test_local_registry_1(setup, teardown):
    cwd = setup()
    registry_name = "ok_registry"
    data_folder = TEST_FOLDER / "data" / registry_name
    try:
        registry = LocalRegistry(
            registry_origin=data_folder,
            registry_name=registry_name,
            registry_folder=cwd
        )

        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "sample_init" in metadata["init"]
        assert "sample_generate" in metadata["generate"]

        destiny_register = cwd / registry_name
        destiny_init = destiny_register / "init"
        destiny_generate = destiny_register / "generate"

        assert destiny_register.is_dir()
        assert destiny_init.is_dir()
        assert destiny_generate.is_dir()

        registry.update_registry()

        assert destiny_register.is_dir()
        assert destiny_init.is_dir()
        assert destiny_generate.is_dir()

    finally:
        teardown()


def test_git_registry_1(setup, teardown):
    cwd = setup()

    registry_name = "ok_registry"
    try:
        registry = GitRegistry(
            registry_url=TEST_REPO,
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "analytics_git" in metadata["init"]
        assert "mlclustering_git" in metadata["generate"]

        destiny_register = cwd / registry_name
        destiny_init = destiny_register / "init"
        destiny_generate = destiny_register / "generate"

        assert destiny_register.is_dir()
        assert destiny_init.is_dir()
        assert destiny_generate.is_dir()

        registry.update_registry()
        metadata = registry.get_templates()

        assert "init" in metadata
        assert "generate" in metadata
        assert "analytics_git" in metadata["init"]
        assert "mlclustering_git" in metadata["generate"]

        assert destiny_register.is_dir()
        assert destiny_init.is_dir()
        assert destiny_generate.is_dir()

        registry = GitRegistry(
            registry_url=TEST_REPO,
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "analytics_git" in metadata["init"]
        assert "mlclustering_git" in metadata["generate"]

        # TODO: Create sample git repository to make a more reproducible test.
    finally:
        teardown()


def test_registry_collection_1(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "git_registry": {
                "open-source": TEST_REPO,
                "ow-private": ""
            },
            "local_registry": {
                "default_registry": TEST_FOLDER / "data" / "ok_registry"
            }
        }
        registry = RegistryCollection.from_config_file(configurations, cwd)

        git_registry = cwd / "open-source"
        local_registry = cwd / "default_registry"
        git_registry_init = git_registry / "init"
        git_registry_generate = git_registry / "generate"
        local_registry_init = local_registry / "init"
        local_registry_generate = local_registry / "generate"

        assert git_registry.is_dir()
        assert local_registry.is_dir()
        assert git_registry_init.is_dir()
        assert git_registry_generate.is_dir()
        assert local_registry_init.is_dir()
        assert local_registry_generate.is_dir()

        metadata = registry.get_templates()

        assert "analytics_git" in metadata['init']
        assert "sample_init" in metadata['init']

    finally:
        teardown()


def test_registry_collection_2(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "local_registry": {
                "default_registry": TEST_FOLDER / "data" / "ok_registry",
                "registry_2": TEST_FOLDER / "data" / "ok_registry"
            }
        }
        with pytest.raises(ValueError):
            RegistryCollection.from_config_file(configurations, cwd)

    finally:
        teardown()
