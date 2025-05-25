import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier

# Paso 1: Cargar datasets

df = pd.read_csv('/content/dataset.csv')
df_val = pd.read_csv('/content/dataset_val.csv')
print(f"Tamaño dataset principal: {df.shape}")
print(f"Tamaño dataset validación externo: {df_val.shape}")

df.head()

# Paso 2: Definir columnas numéricas y categóricas

num_feats = ['MTS2VENTAS_NUM', 'PUERTASREFRIG_NUM', 'CAJONESESTACIONAMIENTO_NUM','LATITUD_NUM','LONGITUD_NUM']
cat_feats = ['ENTORNO_DES', 'SEGMENTO_MAESTRO_DESC', 'LID_UBICACION_TIENDA', 'NIVELSOCIOECONOMICO_DES']

X = df[num_feats + cat_feats]
y = df['TARGET']

X_val = df_val[num_feats + cat_feats]
y_val = df_val['TARGET']

# Paso 4: Definir preprocesador (OneHot + Escalado)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_feats),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_feats)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    stratify=y,
    random_state=42
)
print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

# Paso 5: Definir y entrenar modelos con GridSearch

model_configs = [
    ('Logistic Regression', LogisticRegression(max_iter=1000, random_state=42), {
        'clf__C': [0.01, 0.1, 1, 10],
        'clf__solver': ['lbfgs', 'liblinear']
    }),
    ('Random Forest', RandomForestClassifier(random_state=42), {
        'clf__n_estimators': [100, 200],
        'clf__max_depth': [None, 10, 20]
    }),
    ('KNN', KNeighborsClassifier(), {
        'clf__n_neighbors': [3, 5, 7]
    }),
    ('XGBoost', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42), {
        'clf__n_estimators': [100, 200],
        'clf__learning_rate': [0.01, 0.1, 0.2]
    })
]

best_models = []

for name, model, params in model_configs:
    print(f"\n🔍 Entrenando modelo: {name}")
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('clf', model)
    ])
    grid = GridSearchCV(pipeline, params, cv=5, scoring='f1_macro', n_jobs=-1)
    grid.fit(X_train, y_train)
    print(f"Mejor F1: {grid.best_score_}, Parámetros: {grid.best_params_}")
    filename = f"/content/modelo_{name.lower().replace(' ', '_')}_grid.pkl"
    joblib.dump(grid.best_estimator_, filename)
    best_models.append((name, filename))

# Paso 6: Naive Bayes (sin GridSearch)

pipeline_nb = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('clf', GaussianNB())
])
pipeline_nb.fit(X_train, y_train)
filename_nb = '/content/modelo_naive_bayes.pkl'
joblib.dump(pipeline_nb, filename_nb)
best_models.append(('Naive Bayes', filename_nb))
print("✅ Naive Bayes entrenado y guardado")

# Paso 7: Evaluación final en dataset externo

for model_name, model_path in best_models:
    model = joblib.load(model_path)
    y_pred_val = model.predict(X_val)
    print(f"\n📊 Reporte en VALIDACIÓN EXTERNA para {model_name}")
    print(classification_report(y_val, y_pred_val))

## 📊 Paso 8: Evaluar todos los modelos en dataset externo

for model_name, model_path in best_models:
    model = joblib.load(model_path)
    y_pred_val = model.predict(X_val)
    print(f"\n📊 Reporte en VALIDACIÓN EXTERNA para {model_name}")
    print(classification_report(y_val, y_pred_val))

## 📈 Paso 9: Preparar visualización de resultados

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# Preparar diccionario de métricas
metrics = {
    'Model': [],
    'Accuracy': [],
    'Precision (macro)': [],
    'Recall (macro)': [],
    'F1-score (macro)': []
}

for model_name, model_path in best_models:
    model = joblib.load(model_path)
    y_pred_val = model.predict(X_val)
    metrics['Model'].append(model_name)
    metrics['Accuracy'].append(accuracy_score(y_val, y_pred_val))
    metrics['Precision (macro)'].append(precision_score(y_val, y_pred_val, average='macro', zero_division=0))
    metrics['Recall (macro)'].append(recall_score(y_val, y_pred_val, average='macro'))
    metrics['F1-score (macro)'].append(f1_score(y_val, y_pred_val, average='macro'))

# Convertir a DataFrame
metrics_df = pd.DataFrame(metrics)
print(metrics_df)

## 📊 Paso 10: Graficar resultados comparativos

# Graficar cada métrica
for metric in ['Accuracy', 'Precision (macro)', 'Recall (macro)', 'F1-score (macro)']:
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Model', y=metric, data=metrics_df)
    plt.title(f'Comparación de modelos: {metric}')
    plt.ylim(0, 1)
    plt.ylabel(metric)
    plt.xlabel('Modelo')
    plt.xticks(rotation=45)
    plt.show()