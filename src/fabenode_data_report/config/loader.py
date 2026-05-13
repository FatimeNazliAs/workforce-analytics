from pathlib import Path

import yaml

from .schema import (
    DataColumnsConfig,
    DataLocationConfig,
    DatasetConfig,
    RiskConfig,
    TimeConfig,
    TimeFeatureConfig,
    ShiftConfig,
)


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

    def load_data_columns_config(self) -> DataColumnsConfig:
        return DataColumnsConfig(**self.config["data_cols"])

    def load_data_location_config(self) -> DataLocationConfig:
        return DataLocationConfig(**self.config["data_location"])

    def load_dataset_config(self) -> DatasetConfig:
        return DatasetConfig(**self.config["datasets"])

    def load_risk_config(self) -> RiskConfig:
        return RiskConfig(**self.config)

    def load_time_config(self) -> TimeConfig:
        return TimeConfig(**self.config["time"])

    def load_shift_config(self) -> ShiftConfig:
        return ShiftConfig(**self.config["shifts"])

    def load_time_feature_config(self) -> TimeFeatureConfig:
        return TimeFeatureConfig(**self.config)
