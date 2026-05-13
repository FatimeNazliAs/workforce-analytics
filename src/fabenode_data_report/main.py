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




def main() -> None:

    config_path = Path(__file__).parent / "config"
    config_name = "params.yaml"
    config = ConfigLoader(config_name=config_name, config_path=config_path)

    data_location_config = config.load_data_location_config()
    data_columns_config = config.load_data_columns_config()
    time_feature_config = config.load_time_feature_config()

    loader = DataLoader(data_location_config)
    df = loader.load_data(file_name="user_48_feb02_14_full_hrv.csv", stage="raw")

    validator = DataValidator(data_config=data_columns_config)
    valid_df = validator.filter_valid_rows(df)

    valid_df = add_datetime_columns(valid_df, time_feature_config.time)
    valid_df = add_basic_time_features(valid_df, time_feature_config.time)
    valid_df = add_time_of_day_feature(valid_df, time_feature_config.time)
    valid_df = assign_shift(valid_df, time_feature_config)

    # shift_summary = summarize_shift_assignment(
    #     df=valid_df,
    #     time_col=time_feature_config.time.time_col,
    #     shift_col=time_feature_config.shifts.shift_col,
    # )

    # print(shift_summary)


if __name__ == "__main__":
    main()
