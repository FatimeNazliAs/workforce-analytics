import pandas as pd

from fabenode_data_report.config.schema import DataConfig
from fabenode_data_report.validation_utils import validate_column_exists


class DataValidator:
    """
    Validate and filter physiological report data.

    Parameters
    ----------
    data_config : DataConfig
        Configuration containing data column names and valid values.
    """

    def __init__(self, data_config: DataConfig):
        self.data_config = data_config

    def filter_valid_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter rows that satisfy the configured validity condition.

        Parameters
        ----------
        df : pd.DataFrame
            Input physiological data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing only valid rows.

        Raises
        ------
        KeyError
            If the configured validation column is missing.
        """
        validation_col = self.data_config.data_cols.validation_col
        validation_value = self.data_config.data_cols.validation_choice

        validate_column_exists(df=df, column_name=validation_col)

        return df[df[validation_col] == validation_value].copy()
