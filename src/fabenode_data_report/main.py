# python -m fabenode_data_report.main

from pathlib import Path


from fabenode_data_report.config.loader import ConfigLoader
from fabenode_data_report.data_loader import DataLoader
from fabenode_data_report.time_features import (
    add_basic_time_features,
    add_datetime_columns,
    add_time_of_day_feature,
    assign_shift,
)
from fabenode_data_report.diagnostics import summarize_shift_assignment

from fabenode_data_report.validation import DataValidator
from fabenode_data_report.datasets import DatasetAssembler


def main() -> None:
    config_path = Path(__file__).parent / "config"
    config_loader = ConfigLoader(
        config_name="params.yaml",
        config_path=config_path,
    )

    data_location_config = config_loader.load_data_location_config()
    data_columns_config = config_loader.load_data_columns_config()
    dataset_config = config_loader.load_dataset_config()
    time_feature_config = config_loader.load_time_feature_config()

    dataset_assembler = DatasetAssembler(
        dataset_config=dataset_config,
        data_location_config=data_location_config,
    )

    df = dataset_assembler.load_user_datasets(stage="raw")

    validator = DataValidator(data_config=data_columns_config)
    valid_df = validator.filter_valid_rows(df)

    valid_df = add_datetime_columns(valid_df, time_feature_config.time)
    valid_df = add_basic_time_features(valid_df, time_feature_config.time)
    valid_df = add_time_of_day_feature(valid_df, time_feature_config.time)
    valid_df = assign_shift(valid_df, time_feature_config)

    print(valid_df[dataset_config.user_id_col].value_counts())
    print(
        valid_df.groupby(
            [dataset_config.user_id_col, time_feature_config.shifts.shift_col]
        ).size()
    )


if __name__ == "__main__":
    main()
