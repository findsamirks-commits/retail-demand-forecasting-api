from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Retail Demand Forecasting API", version="1.0")

# Load the trained Random Forest model
model = joblib.load('models/retail_demand_model.joblib')

# Define the expected input data structure using Pydantic
class RetailInput(BaseModel):
    lag_1_month: float
    rolling_mean_3: float

@app.get("/")
def home():
    return {"message": "Welcome to the Retail Demand Forecasting API! Use the /predict endpoint to get sales forecasts."}

@app.post("/predict")
def predict_demand(data: RetailInput):
    # Convert incoming JSON data into a Pandas DataFrame
    input_df = pd.DataFrame([{
        'lag_1_month': data.lag_1_month,
        'rolling_mean_3': data.rolling_mean_3
    }])
    
    # Generate prediction
    prediction = model.predict(input_df)[0]
    
    return {
        "input_features": data.dict(),
        "predicted_sales_demand": round(float(prediction), 4)
    }
