# Dockerfile.prefect
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir \
    pandas \
    scikit-learn \
    pyarrow \
    mlflow \
    prefect \
    numpy \
    scipy

COPY . .

CMD ["python", "prefect_flow.py"]
