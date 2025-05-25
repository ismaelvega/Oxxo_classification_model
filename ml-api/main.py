from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
import joblib

BASE_DIR   = os.path.dirname(__file__)
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_random_forest_grid.pkl")
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_logistic_regression_grid.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "./modelo_knn_grid.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Modelo cargado (joblib) desde", MODEL_PATH)
except Exception as e:
    print("❌ Error cargando el modelo con joblib:", e)
    model = None

class Query(BaseModel):
    lat: float
    lng: float
    entorno: str
    nivelSocioeconomico: str
    ubicacion: str
    segmento: str
    ventasPorMetroCuadrado: float
    puertasRefrigerador: float
    cajonesEstacionamiento: float

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict(q: Query):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible")

    try:
        # 1. Montamos un dict con exactamente los nombres que tu pipeline espera
        row = {
            "LATITUD_NUM":                        q.lat,
            "LONGITUD_NUM":                       q.lng,
            "MTS2VENTAS_NUM":                q.ventasPorMetroCuadrado,
            "PUERTASREFRIG_NUM":              q.puertasRefrigerador,
            "CAJONESESTACIONAMIENTO_NUM":     q.cajonesEstacionamiento,
            "ENTORNO_DES":                    q.entorno,
            "SEGMENTO_MAESTRO_DESC":          q.segmento,
            "LID_UBICACION_TIENDA":           q.ubicacion,
            "NIVELSOCIOECONOMICO_DES":        q.nivelSocioeconomico,
        }

        # 2. Lo convertimos a DataFrame de una sola fila
        X = pd.DataFrame([row])

        # 3. Predicción
        y_pred = model.predict(X)
        print(f"y_pred: {y_pred}")
        profitability = bool(y_pred[0])

        print(f"Model: {model}")
        print(f"Recieved params:  lat={q.lat}, lng={q.lng}, ventasPorMetroCuadrado={q.ventasPorMetroCuadrado}, puertasRefrigerador={q.puertasRefrigerador}, cajonesEstacionamiento={q.cajonesEstacionamiento}, entorno={q.entorno}, segmento={q.segmento}, ubicacion={q.ubicacion}, nivelSocioeconomico={q.nivelSocioeconomico}")
        print("Prediction:", y_pred[0])
        print(f"Profitability: {'Sí' if profitability else 'No'}")

        return {
            "lat": q.lat,
            "lng": q.lng,
            "profitability": profitability
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
