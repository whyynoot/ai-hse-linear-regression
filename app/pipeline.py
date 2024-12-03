from .config import MODEL_PATH 
from .models import Item, PredictionResponse, PredictionSuccessResponse, PredictionErrorResponse
from typing import List
import pandas as pd
from .utils import preprocess_data_for_pipeline
from joblib import load
from pydantic import ValidationError
from functools import wraps

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return PredictionErrorResponse(success=False, error=f"preprocessing error: {str(ve)}")
        except ValidationError as ve:
            return PredictionErrorResponse(success=False, error=f"validation error: {ve.errors()}")
        except Exception as e:
            return PredictionErrorResponse(success=False, error=f"unexpected error: {str(e)}")
    return wrapper

pipeline = load(MODEL_PATH)

@handle_errors
def predict_with_pipeline(items: List[Item]) -> PredictionResponse:
    data = pd.DataFrame([item.model_dump() for item in items])
    processed_data = preprocess_data_for_pipeline(data)
    predictions = pipeline.predict(processed_data)
    return PredictionSuccessResponse(predictions=predictions.tolist())

@handle_errors
def predict_with_pipeline_from_df(df: pd.DataFrame) -> PredictionResponse:
    processed_data = preprocess_data_for_pipeline(df)
    predictions = pipeline.predict(processed_data)
    return PredictionSuccessResponse(predictions=predictions.tolist())