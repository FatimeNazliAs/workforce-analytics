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
        description="Column name for valid HR HRV data.",
    )
    validation_choice: str = Field(
        ...,
        description="Column name for valid HR HRV data.",
    )


class DataLocationConfig(BaseModel):
    """File paths for different data stages."""

    raw_file_path: str = Field(..., description="")
    interim_file_path: str = Field(..., description="")
    processed_file_path: str = Field(..., description="")


class DataConfig(BaseModel):
    data_cols: DataColumnsConfig
    data_location: DataLocationConfig
