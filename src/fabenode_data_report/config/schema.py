from pydantic import BaseModel, Field


class StressRiskConfig(BaseModel):
    score_col: str = Field(..., description="Column containing stress score values.")
    high_threshold: int = Field(..., ge=0)
    critical_threshold: int = Field(..., ge=0)


class HeartRateRiskConfig(BaseModel):
    score_col: str = Field(..., description="Column containing heart rate values.")
    high_threshold: int = Field(..., ge=0)


class RiskConfig(BaseModel):
    stress: StressRiskConfig
    heart_rate: HeartRateRiskConfig


class DataColumnsConfig(BaseModel):
    validation_col: str = Field(
        ...,
        description="Column used to determine whether a row is valid.",
    )
    validation_choice: str = Field(
        ...,
        description="Value indicating a valid row in the validation column.",
    )


class DataLocationConfig(BaseModel):
    """File paths for different data stages."""

    raw_file_path: str = Field(..., description="")
    interim_file_path: str = Field(..., description="")
    processed_file_path: str = Field(..., description="")


class UserDatasetConfig(BaseModel):
    user_id: str
    file_name: str


class DatasetConfig(BaseModel):
    user_id_col: str
    source_file_col: str
    users: list[UserDatasetConfig]



class TimeConfig(BaseModel):
    start_col: str
    finish_col: str
    start_datetime_col: str = "start_time_dt"
    finish_datetime_col: str = "finish_time_dt"
    time_col: str = "time"
    date_col: str = "date"
    hour_col: str = "hour"


class ShiftWindowConfig(BaseModel):
    label: str
    start_time: str
    end_time: str


class ShiftConfig(BaseModel):
    shift_col: str = "shift"
    morning: ShiftWindowConfig
    evening: ShiftWindowConfig


class TimeFeatureConfig(BaseModel):
    time: TimeConfig
    shifts: ShiftConfig
