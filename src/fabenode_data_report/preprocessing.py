from typing import Literal

import pandas as pd

from fabenode_data_report.config.schema import TimeFeatureConfig
from fabenode_data_report.datasets import DatasetAssembler
from fabenode_data_report.time_features import (add_basic_time_features,
                                                add_datetime_columns,
                                                add_time_of_day_feature,
                                                assign_shift)
from fabenode_data_report.validation import DataValidator


def prepare_analysis_dataset(
    dataset_assembler: DatasetAssembler,
    validator: DataValidator,
    time_config: TimeFeatureConfig,
    stage: Literal["raw", "interim", "processed"] = "raw",
) -> pd.DataFrame:
    """
    Prepare the standardized analysis dataset for report metrics.

    Parameters
    ----------
    dataset_assembler : DatasetAssembler
        Object responsible for loading and combining configured user datasets.
    validator : DataValidator
        Validator used to filter rows according to configured validity rules.
    time_config : TimeFeatureConfig
        Configuration used for datetime parsing, time feature creation,
        and shift assignment.
    stage : {"raw", "interim", "processed"}, default="raw"
        Data stage from which configured user files are loaded.

    Returns
    -------
    pd.DataFrame
        Prepared analysis dataframe containing valid rows, user metadata,
        parsed time features, and assigned shift labels.
    """
    df = dataset_assembler.load_user_datasets(stage=stage)

    valid_df = validator.filter_valid_rows(df)

    valid_df = add_datetime_columns(valid_df, time_config.time)
    valid_df = add_basic_time_features(valid_df, time_config.time)
    valid_df = add_time_of_day_feature(valid_df, time_config.time)
    valid_df = assign_shift(valid_df, time_config)

    return valid_df