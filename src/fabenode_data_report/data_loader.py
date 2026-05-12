from pathlib import Path
from typing import Literal

import pandas as pd
from fabenode_data_report.config.schema import DataLocationConfig


class DataLoader:
    """
    Load tabular data files from configured data-stage directories.

    Parameters
    ----------
    config : DataLocationConfig
        Configuration object containing raw, interim, and processed data paths.
    """
    

    def __init__(self, config: DataLocationConfig):
        self.data_config = config

    def load_data(
        self,
        file_name: str,
        stage: Literal["raw", "interim", "processed"] = "raw",
    ) -> pd.DataFrame:
        """
        Load a CSV or Parquet file from a selected data stage.

        Parameters
        ----------
        file_name : str
            Name of the file to load.
        stage : {"raw", "interim", "processed"}, default="raw"
            Data stage directory where the file is located.

        Returns
        -------
        pd.DataFrame
            Loaded tabular data.

        Raises
        ------
        FileNotFoundError
            If the requested file does not exist.
        ValueError
            If the stage or file extension is unsupported.
        KeyError
            If the configured stage path is missing.
        """

        stage_map = {
            "raw": "raw_file_path",
            "interim": "interim_file_path",
            "processed": "processed_file_path",
        }

        if stage not in stage_map:
            raise ValueError(
                f"Invalid stage '{stage}'. Expected one of {list(stage_map.keys())}."
            )

        folder_path = getattr(self.data_config, stage_map[stage], None)

        if not folder_path:
            raise KeyError(f"Configuration missing path for '{stage_map[stage]}'")

        full_file_path = Path(folder_path) / file_name

        if not full_file_path.is_file():
            raise FileNotFoundError(f"Data file not found: {full_file_path}")

        ext = full_file_path.suffix.lower()
        if ext == ".parquet":
            df = pd.read_parquet(full_file_path)
        elif ext == ".csv":
            df = pd.read_csv(full_file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        return df
