import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import requests
import joblib
import os

# Configuración
URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet"
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
FILE_PATH = DATA_DIR / "yellow_tripdata_2023-03.parquet"
MODEL_PATH = Path("model.pkl")

# Descargar si no existe
if not FILE_PATH.exists():
    print(f"⬇️ Downloading dataset to {FILE_PATH}...")
    response = requests.get(URL)
    with open(FILE_PATH, "wb") as f:
        f.write(response.content)
    print("✅ Download complete.")
else:
    print("📂 File already exists, skipping download.")

# Cargar datos
df = pd.read_parquet(FILE_PATH)

# Calcular duración
df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
df.duration = df.duration.dt.total_seconds() / 60

# Filtrar viajes extremos
df = df[(df.duration >= 1) & (df.duration <= 60)]

# Vectorizar features
categorical = ['PULocationID', 'DOLocationID']
numerical = ['trip_distance']
df[categorical] = df[categorical].astype(str)

train_dicts = df[categorical + numerical].to_dict(orient='records')
dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)
y_train = df['duration'].values

# Entrenar modelo
lr = LinearRegression()
lr.fit(X_train, y_train)

# Evaluar
y_pred = lr.predict(X_train)
rmse = np.sqrt(mean_squared_error(y_train, y_pred))

# Guardar modelo
joblib.dump(lr, MODEL_PATH)

# Validar tamaño
model_size = os.path.getsize(MODEL_PATH)

# Resultados
print(f"📊 Records loaded: {len(df):,}")
print(f"✅ Intercept: {lr.intercept_:.2f}")
print(f"✅ RMSE (train): {rmse:.2f}")
print(f"📦 Model saved to {MODEL_PATH}")
print(f"📏 Model size: {model_size} bytes")
