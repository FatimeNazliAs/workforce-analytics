from collections.abc import Sequence

import pandas as pd


def validate_dataframe(df: pd.DataFrame, allow_empty: bool = False) -> None:
    """
    Validate that the input is a pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.
    allow_empty : bool, default=False
        Whether empty DataFrames are allowed.

    Raises
    ------
    TypeError
        If input is not a pandas DataFrame.
    ValueError
        If DataFrame is empty and allow_empty is False.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    if not allow_empty and df.empty:
        raise ValueError("df cannot be empty.")


def validate_column_exists(df: pd.DataFrame, column_name: str) -> None:
    """
    Validate that a column exists in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to check.
    column_name : str
        Required column name.

    Raises
    ------
    KeyError
        If the column is missing.
    """
    validate_dataframe(df)

    if column_name not in df.columns:
        raise KeyError(f"Missing column: {column_name}")


def validate_columns_exist(df: pd.DataFrame, column_names: Sequence[str]) -> None:
    """
    Validate that multiple columns exist in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to check.
    column_names : Sequence[str]
        Required column names.

    Raises
    ------
    KeyError
        If one or more columns are missing.
    """
    validate_dataframe(df)

    missing_columns = [column for column in column_names if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing columns: {missing_columns}")


def validate_non_empty_string(value: str, name: str) -> None:
    """
    Validate that a value is a non-empty string.

    Parameters
    ----------
    value : str
        String value to validate.
    name : str
        Parameter name used in error messages.

    Raises
    ------
    TypeError
        If value is not a string.
    ValueError
        If value is empty.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")

    if not value.strip():
        raise ValueError(f"{name} cannot be empty.")