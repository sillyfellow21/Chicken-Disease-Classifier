from pathlib import Path
from typing import Tuple
from pydantic import BaseModel
import yaml
from pydantic_settings import BaseSettings

class DataIngestionConfig(BaseModel):
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

class PrepareModelConfig(BaseModel):
    root_dir: Path
    base_model_path: Path
    updated_model_path: Path

class TrainingConfig(BaseModel):
    root_dir: Path
    trained_model_path: Path
    metrics_path: Path

class AppConfig(BaseModel):
    artifacts_root: Path
    data_ingestion: DataIngestionConfig
    prepare_model: PrepareModelConfig
    training: TrainingConfig

class Params(BaseModel):
    epochs: int
    batch_size: int
    learning_rate: float
    image_size: Tuple[int, int]
    classes: int
    backbone: str

class Settings(BaseSettings):
    MODEL_PATH: str = "artifacts/training/model.pt"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""

    class Config:
        env_file = ".env"

def load_config() -> AppConfig:
    with open("config/config.yaml", "r") as f:
        config_dict = yaml.safe_load(f)
    return AppConfig(**config_dict)

def load_params() -> Params:
    with open("params.yaml", "r") as f:
        params_dict = yaml.safe_load(f)
    return Params(**params_dict)

def get_settings() -> Settings:
    return Settings()
