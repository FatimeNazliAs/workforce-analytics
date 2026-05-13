from datetime import datetime, time

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

from fabenode_data_report.config.schema import (ShiftConfig, TimeConfig,
                                                TimeFeatureConfig)
from fabenode_data_report.validation_utils import validate_column_exists


def add_datetime_columns(df: pd.DataFrame, config: TimeConfig) -> pd.DataFrame:
    """
    Add parsed datetime columns from raw start and finish time columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing raw timestamp columns.
    config : TimeConfig
        Time feature configuration containing input and output column names.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataframe with parsed datetime columns added.

    Raises
    ------
    KeyError
        If configured raw timestamp columns are missing.
    ValueError
        If timestamp parsing fails.
    """
    df = df.copy()

    validate_column_exists(df, config.start_col)
    validate_column_exists(df, config.finish_col)

    df[config.start_datetime_col] = pd.to_datetime(
        df[config.start_col],
        errors="raise",
    )
    df[config.finish_datetime_col] = pd.to_datetime(
        df[config.finish_col],
        errors="raise",
    )

    return df


def add_basic_time_features(df: pd.DataFrame, config: TimeConfig) -> pd.DataFrame:
    """
    Add basic date and hour features from the parsed start datetime column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing a parsed start datetime column.
    config : TimeConfig
        Time feature configuration containing datetime and output feature names.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataframe with date and hour columns added.

    Raises
    ------
    KeyError
        If the configured start datetime column is missing.
    TypeError
        If the configured start datetime column is not datetime typed.
    """
    df = df.copy()

    validate_column_exists(df, config.start_datetime_col)

    if not is_datetime64_any_dtype(df[config.start_datetime_col]):
        raise TypeError(
            f"Column '{config.start_datetime_col}' must be datetime dtype. "
            "Run add_datetime_columns() first."
        )

    df[config.hour_col] = df[config.start_datetime_col].dt.hour
    df[config.date_col] = df[config.start_datetime_col].dt.date

    return df


def add_time_of_day_feature(
    df: pd.DataFrame,
    config: TimeConfig,
) -> pd.DataFrame:
    """
    Add time-of-day feature from the parsed start datetime column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing the parsed start datetime column.
    config : TimeConfig
        Time feature configuration containing input and output column names.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataframe with a time-of-day column added.

    Raises
    ------
    KeyError
        If the configured start datetime column is missing.
    TypeError
        If the configured start datetime column is not datetime typed.
    """
    df = df.copy()

    validate_column_exists(df, config.start_datetime_col)

    if not is_datetime64_any_dtype(df[config.start_datetime_col]):
        raise TypeError(
            f"Column '{config.start_datetime_col}' must be datetime dtype. "
            "Run add_datetime_columns() first."
        )

    df[config.time_col] = df[config.start_datetime_col].dt.time

    return df


def _parse_time_string(time_string: str) -> time:
    """
    Parse an HH:MM time string into a Python time object.

    Parameters
    ----------
    time_string : str
        Time string in HH:MM format.

    Returns
    -------
    datetime.time
        Parsed time object.
    """
    return datetime.strptime(time_string, "%H:%M").time()


def _is_time_in_window(current_time: time, start_time, end_time)-> bool:
    """
    Check whether a time value falls inside a shift window.

    Parameters
    ----------
    current_time : datetime.time
        Time value to evaluate.
    start_time : datetime.time
        Inclusive start time of the window.
    end_time : datetime.time
        Exclusive end time of the window.

    Returns
    -------
    bool
        True if current_time is inside the window, otherwise False.
    """
    if end_time == time(0, 0):
        return current_time >= start_time

    return start_time <= current_time < end_time


def _assign_single_shift(current_time: time, config: ShiftConfig)-> str:
    """
    Assign a shift label for a single time value.

    Parameters
    ----------
    current_time : datetime.time
        Time value to assign.
    config : ShiftConfig
        Shift configuration containing shift windows and labels.

    Returns
    -------
    str
        Matching shift label, or "unknown" if no shift window matches.
    """

    morning_start = _parse_time_string(config.morning.start_time)
    morning_end = _parse_time_string(config.morning.end_time)

    if _is_time_in_window(current_time, morning_start, morning_end):
        return config.morning.label

    evening_start = _parse_time_string(config.evening.start_time)
    evening_end = _parse_time_string(config.evening.end_time)

    if _is_time_in_window(current_time, evening_start, evening_end):
        return config.evening.label

    return "unknown"


def assign_shift(df: pd.DataFrame, config: TimeFeatureConfig)-> pd.DataFrame:
    """
    Add shift labels to rows based on configured shift windows.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing a time-of-day column.
    config : TimeFeatureConfig
        Time and shift configuration.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataframe with a shift column added.

    Raises
    ------
    KeyError
        If the configured time column is missing.
    """
    df = df.copy()
    validate_column_exists(df, config.time.time_col)
    df[config.shifts.shift_col] = df[config.time.time_col].apply(
        lambda current_time: _assign_single_shift(current_time, config.shifts)
    )
    return df
