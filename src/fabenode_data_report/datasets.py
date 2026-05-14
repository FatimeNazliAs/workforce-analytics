import pandas as pd
from typing import Literal

from fabenode_data_report.config.schema import (
    DatasetConfig,
    DataLocationConfig,
    UserDatasetConfig,
)
from fabenode_data_report.data_loader import DataLoader


class DatasetAssembler:
    """
    Assemble one or more configured user datasets into a single dataframe.

    Parameters
    ----------
    dataset_config : DatasetConfig
        Configuration containing user dataset entries and metadata column names.
    data_location_config : DataLocationConfig
        Configuration containing raw, interim, and processed data directories.
    """

    def __init__(
        self,
        dataset_config: DatasetConfig,
        data_location_config: DataLocationConfig,
    ) -> None:
        self.dataset_config = dataset_config
        self.data_loader = DataLoader(data_location_config)

    def load_user_dataset(
        self,
        user_config: UserDatasetConfig,
        stage: Literal["raw", "interim", "processed"] = "raw",
    ) -> pd.DataFrame:
        """
        Load a single user dataset and attach metadata columns.

        Parameters
        ----------
        user_config : UserDatasetConfig
            Configuration for one user data file.
        stage : {"raw", "interim", "processed"}, default="raw"
            Data stage directory where the file is located.

        Returns
        -------
        pd.DataFrame
            User dataframe with user and source-file metadata columns.
        """
        df = self.data_loader.load_data(
            file_name=user_config.file_name,
            stage=stage,
        )

        df = df.copy()
        df[self.dataset_config.user_id_col] = user_config.user_id
        df[self.dataset_config.source_file_col] = user_config.file_name

        return df

    def load_user_datasets(
        self,
        stage: Literal["raw", "interim", "processed"] = "raw",
    ) -> pd.DataFrame:
        """
        Load and combine all configured user datasets.

        Parameters
        ----------
        stage : {"raw", "interim", "processed"}, default="raw"
            Data stage directory where the file is located.

        Returns
        -------
        pd.DataFrame
            Combined dataframe containing all configured users.
        """
        dataframes = [
            self.load_user_dataset(user_config=user_config, stage=stage)
            for user_config in self.dataset_config.users
        ]

        return pd.concat(dataframes, ignore_index=True)