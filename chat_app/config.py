import json
from pathlib import Path

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class ConfigModel(BaseSettings):
    selected_model: str | None = None
    top_p: int = Field(default=1, ge=0.0, le=1)
    top_k: int = Field(default=1, ge=0.0, le=1)
    temperature: float = Field(default=0.8, ge=0.0, le=1)
    database_url: str = Field(default="chat_app.db")
    # Add any 3rd party API keys in the future.


class Config:
    def __init__(self, config_file: str = "chat_config.json"):
        self.config_file = config_file

    def _config_file_init(self) -> tuple[bool, bool]:
        """Checks if the config file exists and creates it if it doesn't."""
        config_file_path = Path(self.config_file)
        if not config_file_path.exists():
            config_file_path.touch()
            with open(config_file_path, "w") as file:
                json.dump(ConfigModel().model_dump(), file, indent=4)

            print(f"Configuration file created: {config_file_path}")
            created = True
            exists = False
        else:
            created, exists = False, True

        return (created, exists)

    def write(self, key, value):
        """Write to config file"""

        # If json config is not empty
        if Path(self.config_file).stat().st_size != 0:
            config = self.get()
            updated_config = config.model_copy(update={key: value})
            validated_config = ConfigModel(**updated_config.model_dump())
        else:

            validated_config = ConfigModel(**{key: value})

        try:
            with open(self.config_file, "w") as file:
                json.dump(validated_config.model_dump(), file, indent=4)
        except Exception as err:
            raise Exception(
                f"Error writing to configuration to {self.config_file}: {err}"
            )

    def get(self) -> ConfigModel | None:
        """Get data from config file."""
        created, exists = self._config_file_init()
        if created or Path(self.config_file).stat().st_size == 0:
            # If it was just created, the config will be empty
            return None

        try:
            with open(self.config_file, "r") as file:
                config = json.load(file)
                if not config:
                    return None
                return ConfigModel(**config)

        except (json.JSONDecodeError, ValidationError) as err:
            raise Exception(
                f"Error fetching configuration from {self.config_file}: {err}"
            )


config = Config()
