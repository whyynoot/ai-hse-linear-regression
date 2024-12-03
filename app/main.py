from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
import io 
from typing import List
from .models import Item
from .pipeline import predict_with_pipeline, predict_with_pipeline_from_df
import pandas as pd
from .models import PredictionResponse, PredictionErrorResponse

app = FastAPI()

@app.post("/predict_item", response_model=PredictionResponse)
def predict_item(item: Item):
    return predict_with_pipeline([item])

@app.post("/predict_items", response_model=PredictionResponse)
def predict_items(items: List[Item]):
    return predict_with_pipeline(items)

@app.post("/predict_items_csv", response_model=PredictionResponse)
async def predict_items_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    result = predict_with_pipeline_from_df(df)

    if isinstance(result, PredictionErrorResponse):
        raise HTTPException(status_code=400, detail=result.error)

    df['predicted_price'] = result.predictions
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    response = StreamingResponse(stream, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response