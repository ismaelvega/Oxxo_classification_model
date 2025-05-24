from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Query(BaseModel):
    lat: float
    lng: float
    category: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predict")
def predict(q: Query):
    # a simple hello world endpoint
    try:
        lat = q.lat
        lng = q.lng
        # Just as an  example return profitability equals true if the sum of lat and lng is greater than 0 and false otherwise
        profitability = lat + lng > 0
        # Here you would typically call your model to get a prediction
        # For demonstration, we will just return the input values
        print(f"Received lat: {lat}, lng: {lng}")
        return {"lat": lat, "lng": lng, "profitability": profitability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))