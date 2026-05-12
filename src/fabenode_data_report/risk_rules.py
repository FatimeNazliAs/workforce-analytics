import pandas as pd

from fabenode_data_report.config.schema import RiskConfig, StressRiskConfig
from fabenode_data_report.validation_utils import (
    validate_column_exists,
)


def is_critical_stress(df: pd.DataFrame, config: StressRiskConfig) -> pd.Series:
    """
    Identify rows where stress score exceeds the critical threshold.

    Parameters
    ----------
    df : pd.DataFrame
        Input physiological data.
    config : StressRiskConfig
        Stress threshold configuration.

    Returns
    -------
    pd.Series
        Boolean mask indicating critical stress rows.
    """

    stress_score_col = config.score_col
    validate_column_exists(df, stress_score_col)
    return df[stress_score_col] >= config.critical_threshold


def is_critical_event(
    df: pd.DataFrame,
    config: RiskConfig,
) -> pd.Series:
    """
    Identify rows satisfying the critical event condition.

    Parameters
    ----------
    df : pd.DataFrame
        Input physiological data.
    config : RiskConfig
        Risk threshold configuration.

    Returns
    -------
    pd.Series
        Boolean mask indicating critical event rows.
    """
    critical_stress_mask = is_critical_stress(
        df=df,
        config=config.stress,
    )

    hr_col = config.heart_rate.score_col

    validate_column_exists(df, hr_col)

    critical_hr_mask = df[hr_col] >= config.heart_rate.high_threshold

    return critical_stress_mask & critical_hr_mask


def is_high_load(df: pd.DataFrame, config: RiskConfig) -> pd.Series:
    """
    Identify rows satisfying the high-load condition.

    High load is defined as:
    - stress score >= high stress threshold
    OR
    - heart rate >= high heart rate threshold

    Parameters
    ----------
    df : pd.DataFrame
        Input physiological data.
    config : RiskConfig
        Risk threshold configuration.

    Returns
    -------
    pd.Series
        Boolean mask indicating high-load rows.
    """
    stress_score_col = config.stress.score_col
    validate_column_exists(df, stress_score_col)

    high_stress_mask = df[stress_score_col] >= config.stress.high_threshold

    hr_col = config.heart_rate.score_col
    validate_column_exists(df, hr_col)

    high_hr_mask = df[hr_col] >= config.heart_rate.high_threshold

    return high_stress_mask | high_hr_mask