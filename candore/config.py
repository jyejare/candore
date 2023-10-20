from pathlib import Path, PurePath
from dynaconf import Dynaconf
from dynaconf.validator import Validator


CURRENT_DIRECTORY = Path().resolve()
settings_file = PurePath(CURRENT_DIRECTORY, 'settings.yaml')
components_file = PurePath(CURRENT_DIRECTORY, 'components.yaml')
# Initialize and Configure Settings
settings = Dynaconf(
    core_loaders=["YAML"],
    envvar_prefix="CANDORE",
    settings_files=[settings_file, components_file],
    envless_mode=True,
    lowercase_read=True,
)


def validate_settings():
    provider_settings = [
        f"candore.{setting_key}" for setting_key in settings.to_dict().get('CANDORE')
    ]
    settings.validators.register(Validator(*provider_settings, ne=None))
    try:
        settings.validators.validate()
    except Exception as ecc:
        raise ecc


validate_settings()
