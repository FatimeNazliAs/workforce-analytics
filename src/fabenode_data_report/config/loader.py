from pathlib import Path
from .schema import DataConfig, RiskConfig
import yaml


class ConfigLoader:
    def __init__(self, config_name: str, config_path: str = "src/config"):
        self.config_name = config_name
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Load a YAML configuration file.

        Returns
        -------
        dict
            Parsed configuration as a dictionary.

        Raises
        ------
        FileNotFoundError
            If the configuration file does not exist.
        yaml.YAMLError
            If the YAML file is invalid.
        """
        config_full_path = self.config_path / self.config_name

        if not config_full_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_full_path}")

        with open(config_full_path, "r") as f:
            try:
                config = yaml.safe_load(f) or {}
                return config
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Invalid YAML in {config_full_path}: {e}")

    def load_data_config(self) -> DataConfig:
        return DataConfig(**self.config)

    def load_risk_config(self) -> RiskConfig:
        return RiskConfig(**self.config)
