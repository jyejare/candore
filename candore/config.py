from pathlib import Path, PurePath
from dynaconf import Dynaconf
from dynaconf.validator import Validator

CURRENT_DIRECTORY = Path().resolve()
settings_file = PurePath(CURRENT_DIRECTORY, 'settings.yaml')
conf_dir = PurePath(CURRENT_DIRECTORY, 'conf')
# Initialize and Configure Settings
settings = Dynaconf(
    core_loaders=["YAML"],
    envvar_prefix="CANDORE",
    settings_file=settings_file,
    preload=[f"{conf_dir}/*.yaml"],
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
