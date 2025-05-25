from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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
    # a simple hello world endpoint
    try:
        lat = q.lat
        lng = q.lng
        entorno = q.entorno
        nivelSocioeconomico = q.nivelSocioeconomico
        ubicacion = q.ubicacion
        segmento = q.segmento
        ventasPorMetroCuadrado = q.ventasPorMetroCuadrado
        puertasRefrigerador = q.puertasRefrigerador
        cajonesEstacionamiento = q.cajonesEstacionamiento
        # Here you would typically call your model to get a prediction
        profitability = True # dummy value
        # For demonstration, we will just return the input values
        print(f"Received lat: {lat}, lng: {lng}, entorno: {entorno}, nivelSocioeconomico: {nivelSocioeconomico}, ubicacion: {ubicacion}, segmento: {segmento}, ventasPorMetroCuadrado: {ventasPorMetroCuadrado}, puertasRefrigerador: {puertasRefrigerador}, cajonesEstacionamiento: {cajonesEstacionamiento}")

        return {"lat": lat, "lng": lng, "profitability": profitability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))