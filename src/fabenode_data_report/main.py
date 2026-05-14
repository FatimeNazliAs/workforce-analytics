# python -m fabenode_data_report.main

from pathlib import Path

from fabenode_data_report.config.loader import ConfigLoader
from fabenode_data_report.datasets import DatasetAssembler
from fabenode_data_report.preprocessing import prepare_analysis_dataset
from fabenode_data_report.validation import DataValidator
from fabenode_data_report.data_writer import DataWriter


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

    validator = DataValidator(data_config=data_columns_config)

    prepared_df = prepare_analysis_dataset(
        dataset_assembler=dataset_assembler,
        validator=validator,
        time_config=time_feature_config,
        stage="raw",
    )
    data_writer = DataWriter(data_location_config)
    data_writer.save_data(prepared_df, "prepared_analysis_dataset.csv", "interim")


if __name__ == "__main__":
    main()
