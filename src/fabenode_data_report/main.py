# python -m fabenode_data_report.main

from pathlib import Path

from fabenode_data_report.config.loader import ConfigLoader
from fabenode_data_report.validation import DataValidator
from fabenode_data_report.data_loader import DataLoader
from fabenode_data_report.risk_rules import is_critical_stress, is_critical_event


def main():
    config_path = Path(__file__).parent / "config"
    config_name = "params.yaml"
    config = ConfigLoader(config_name=config_name, config_path=config_path)

    data_config = config.load_data_config()

    loader = DataLoader(data_config.data_location)
    df = loader.load_data(file_name="user_48_feb02_14_full_hrv.csv", stage="raw")

    validator = DataValidator(data_config=data_config)
    valid_df = validator.filter_valid_rows(df)

    risk_config = config.load_risk_config()

    critical_stress_mask = is_critical_stress(df, risk_config.stress)
    critical_stress_df = df[critical_stress_mask]

    critical_event_mask = is_critical_event(df, risk_config)
    critical_event_df = df[critical_event_mask]
    print(critical_event_df["hr"].unique())
    print(critical_event_df["stress_score"].unique())



if __name__ == "__main__":
    main()
