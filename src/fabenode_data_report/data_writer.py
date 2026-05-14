from pathlib import Path
from typing import Literal

import pandas as pd

from fabenode_data_report.config.schema import DataLocationConfig
from fabenode_data_report.validation_utils import (
    validate_dataframe,
    validate_non_empty_string,
)


class DataWriter:
    """
    Save tabular data files to configured data-stage directories.

    Parameters
    ----------
    config : DataLocationConfig
        Configuration object containing raw, interim, and processed data paths.
    """

    def __init__(self, config: DataLocationConfig) -> None:
        self.data_location_config = config

    def _get_folder_path(
        self,
        stage: Literal["raw", "interim", "processed"],
    ) -> Path:
        stage_map = {
            "raw": "raw_file_path",
            "interim": "interim_file_path",
            "processed": "processed_file_path",
        }

        if stage not in stage_map:
            raise ValueError(
                f"Invalid stage '{stage}'. Expected one of {list(stage_map.keys())}."
            )

        folder_path = getattr(self.data_location_config, stage_map[stage], None)

        if not folder_path:
            raise KeyError(f"Configuration missing path for '{stage_map[stage]}'")

        return Path(folder_path)

    def save_data(
        self,
        df: pd.DataFrame,
        file_name: str,
        stage: Literal["raw", "interim", "processed"],
    ) -> Path:
        """
        Save a dataframe as CSV or Parquet to a configured data-stage directory.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to save.
        file_name : str
            Output file name including extension.
        stage : {"raw", "interim", "processed"}, default="interim"
            Data stage directory where the file will be saved.

        Returns
        -------
        pathlib.Path
            Full path of the saved file.

        Raises
        ------
        ValueError
            If the file extension is unsupported.
        """
        validate_dataframe(df)
        validate_non_empty_string(file_name, "file_name")

        folder_path = self._get_folder_path(stage=stage)
        folder_path.mkdir(parents=True, exist_ok=True)

        full_file_path = folder_path / file_name
        extension = full_file_path.suffix.lower()

        if extension == ".parquet":
            df.to_parquet(full_file_path)
        elif extension == ".csv":
            df.to_csv(full_file_path, index=False)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")

        return full_file_path
