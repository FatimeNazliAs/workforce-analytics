import pandas as pd


def summarize_shift_assignment(
    df: pd.DataFrame,
    time_col: str,
    shift_col: str,
) -> pd.DataFrame:
    """
    Summarize assigned shifts using min, max, and count of time values.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing assigned shift labels.
    time_col : str
        Column containing time-of-day values.
    shift_col : str
        Column containing shift labels.

    Returns
    -------
    pd.DataFrame
        Summary table with min time, max time, and row count per shift.
    """
    return df.groupby(shift_col)[time_col].agg(["min", "max", "count"])


def get_shift_boundary_rows(
    df: pd.DataFrame,
    time_col: str,
    shift_col: str,
    start_time,
    end_time,
) -> pd.DataFrame:
    """
    Return rows within a selected time-of-day interval.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing time-of-day and shift columns.
    time_col : str
        Column containing time-of-day values.
    shift_col : str
        Column containing shift labels.
    start_time : datetime.time
        Inclusive start time for inspection.
    end_time : datetime.time
        Inclusive end time for inspection.

    Returns
    -------
    pd.DataFrame
        Rows within the requested time interval.
    """
    return df[
        (df[time_col] >= start_time)
        & (df[time_col] <= end_time)
    ][[time_col, shift_col]]


if __name__ == "__main__":
    pass
    # summary = summarize_shift_assignment(df, "time", "shift")
    # print(summary)

    # boundary_rows = get_shift_boundary_rows(
    #     df=df,
    #     time_col="time",
    #     shift_col="shift",
    #     start_time=time(14, 25),
    #     end_time=time(14, 35),
    # )
    # print(boundary_rows)

