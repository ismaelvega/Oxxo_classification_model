# 🏪 Modelo de Clasificación OXXO

Sistema de predicción de rentabilidad para ubicaciones de tiendas OXXO usando machine learning y una interfaz web interactiva.

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema completo para predecir la rentabilidad de ubicaciones potenciales de tiendas OXXO. Utiliza múltiples algoritmos de machine learning entrenados con datos históricos y características socioeconómicas, geográficas y comerciales.

### Características Principales

- 🤖 **API de Machine Learning**: API REST construida con FastAPI que sirve modelos de clasificación
- 🗺️ **Interfaz Web Interactiva**: Aplicación Next.js con mapa interactivo de Google Maps
- 📊 **Múltiples Modelos**: Soporte para 5 algoritmos diferentes (KNN, Random Forest, Regresión Logística, Naive Bayes, XGBoost)
- 🎯 **Predicción en Tiempo Real**: Evaluación instantánea de rentabilidad basada en parámetros de entrada

## 🏗️ Arquitectura del Sistema

```
├── ml-api/              # API de Machine Learning (FastAPI)
├── ui/                  # Interfaz de usuario (Next.js)
└── info/               # Documentación del proyecto
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Node.js 18+
- npm o yarn

### 1. Configuración del Backend (API ML)

```bash
# Navegar al directorio de la API
cd ml-api

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración del Frontend (UI)

```bash
# Navegar al directorio de la UI
cd ui

# Instalar dependencias
npm install
```

### 3. Configuración de Google Maps API

1. Obtén una clave de API de Google Maps
2. Crea un archivo `.env.local` en el directorio `ui/`:

```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=tu_clave_de_api_aqui
```

## 🎯 Uso del Sistema

### Ejecutar el Backend

```bash
cd ml-api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://localhost:8000`

### Ejecutar el Frontend

```bash
cd ui
npm run dev
```

La aplicación web estará disponible en: `http://localhost:3000`

### Usando la Interfaz Web

1. **Seleccionar ubicación**: Haz clic en el mapa o introduce manualmente las coordenadas
2. **Configurar parámetros**:
   - **Ventas por m²**: Proyección de ventas por metro cuadrado
   - **Puertas de refrigerador**: Número de puertas de refrigerador planeadas
   - **Cajones de estacionamiento**: Espacios de estacionamiento disponibles
   - **Entorno**: Tipo de entorno (BASE, HOGAR, PEATONAL, RECESO)
   - **Nivel socioeconómico**: Clasificación del área (AB, B, BC, C, CD, D)
   - **Ubicación**: Tipo de ubicación de tienda
   - **Segmento**: Clasificación del segmento de mercado

3. **Obtener predicción**: Haz clic en "Predict" para obtener el análisis de rentabilidad

## 🤖 Modelos de Machine Learning

El sistema incluye 5 modelos diferentes optimizados con GridSearchCV:

| Modelo | Descripción | Uso Actual |
|--------|-------------|------------|
| **K-Nearest Neighbors** | Clasificación basada en vecinos más cercanos | ✅ Activo |
| **Random Forest** | Ensamble de árboles de decisión | ⚪ Disponible |
| **Regresión Logística** | Modelo lineal probabilístico | ⚪ Disponible |
| **Naive Bayes** | Clasificador probabilístico | ⚪ Disponible |
| **XGBoost** | Gradient boosting optimizado | ⚪ Disponible |

### Cambiar de Modelo

Para usar un modelo diferente, edita `ml-api/main.py` y cambia la línea:

```python
# Descomenta el modelo que quieras usar:
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_random_forest_grid.pkl")
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_logistic_regression_grid.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "./modelo_knn_grid.pkl")  # Actualmente activo
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_naive_bayes.pkl")
# MODEL_PATH = os.path.join(BASE_DIR, "./modelo_xgboost_grid.pkl")
```

## 📊 Parámetros de Entrada

### Parámetros Numéricos
- **Latitud/Longitud**: Coordenadas geográficas de la ubicación
- **Ventas por Metro Cuadrado**: Proyección de ingresos por m² (valor por defecto: 42,000)
- **Puertas Refrigerador**: Número de puertas de refrigerador (valor por defecto: 4)
- **Cajones Estacionamiento**: Espacios de estacionamiento (valor por defecto: 6)

### Parámetros Categóricos
- **Entorno**: BASE, HOGAR, PEATONAL, RECESO
- **Nivel Socioeconómico**: AB, B, BC, C, CD, D
- **Ubicación**: UT_CARRETERA_GAS, UT_DENSIDAD, UT_GAS_URBANA, UT_TRAFICO_PEATONAL, UT_TRAFICO_VEHICULAR
- **Segmento**: BARRIO COMPETIDO, CLÁSICO, HOGAR REUNIÓN, OFICINISTAS, PARADA TÉCNICA

## 🔧 API Endpoints

### POST `/predict`

Realiza predicción de rentabilidad para una ubicación específica.

**Request Body:**
```json
{
  "lat": 19.4326,
  "lng": -99.1332,
  "entorno": "PEATONAL",
  "nivelSocioeconomico": "C",
  "ubicacion": "UT_TRAFICO_PEATONAL",
  "segmento": "CLÁSICO",
  "ventasPorMetroCuadrado": 45000,
  "puertasRefrigerador": 4,
  "cajonesEstacionamiento": 8
}
```

**Response:**
```json
{
  "lat": 19.4326,
  "lng": -99.1332,
  "profitability": true
}
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web para Python
- **scikit-learn**: Biblioteca de machine learning
- **pandas**: Manipulación de datos
- **joblib**: Serialización de modelos
- **XGBoost**: Gradient boosting framework

### Frontend
- **Next.js**: Framework de React
- **React**: Biblioteca de interfaz de usuario
- **Google Maps API**: Integración de mapas interactivos
- **Tailwind CSS**: Framework de CSS

## 📈 Rendimiento de los Modelos

Los modelos han sido evaluados en un dataset de validación externo con las siguientes métricas:
- Accuracy
- Precision (macro)
- Recall (macro)
- F1-score (macro)

Para ver métricas detalladas, ejecuta el script de entrenamiento `modelo_clasificacion_oxxo.py`.

## 🔄 Desarrollo y Contribución

### Estructura de Branching
- `main`: Rama principal estable
- `website`: Rama de desarrollo de la interfaz web

### Para Contribuir
1. Haz fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit
4. Push a tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📝 Notas Adicionales

- El sistema actualmente utiliza el modelo KNN por defecto
- Los modelos están pre-entrenados y serializados como archivos `.pkl`
- La API incluye manejo de errores y validación de entrada
- El frontend incluye validación de formularios en tiempo real

## 🆘 Resolución de Problemas

### Problemas Comunes

1. **Error de CORS**: Asegúrate de que la API esté ejecutándose en el puerto 8000
2. **Google Maps no carga**: Verifica que la clave de API esté configurada correctamente
3. **Modelo no carga**: Verifica que los archivos `.pkl` estén en el directorio `ml-api/`

### Logs y Debugging

Los logs de la API se muestran en la consola donde ejecutaste `uvicorn`. Para debugging detallado, revisa las salidas de consola en ambos servicios.
