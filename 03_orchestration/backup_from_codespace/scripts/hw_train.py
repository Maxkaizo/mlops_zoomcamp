import pandas as pd
import argparse
import joblib
import os
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
import mlflow
from mlflow.models.signature import infer_signature

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mlflow_uri", required=True)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--input_file", required=True)
    args = parser.parse_args()

    # MLflow config
    mlflow.set_tracking_uri(args.mlflow_uri)
    mlflow.set_experiment(args.experiment)

    df = pd.read_parquet(args.input_file)

    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']
    df[categorical] = df[categorical].astype(str)

    train_dicts = df[categorical + numerical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    y_train = df['duration'].values

    with mlflow.start_run():
        print("📍 Run ID:", mlflow.active_run().info.run_id)
        print("📍 Artifact URI:", mlflow.get_artifact_uri())

        # Log parameters
        mlflow.log_param("model_type", "LinearRegression")

        # Train model
        lr = LinearRegression()
        lr.fit(X_train, y_train)

        # Evaluation
        y_pred = lr.predict(X_train)
        rmse = root_mean_squared_error(y_train, y_pred)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("intercept", lr.intercept_)

        print(f"✅ RMSE: {rmse:.2f}")
        print(f"📌 Intercept: {lr.intercept_:.2f}")

        # Save and log model
        joblib.dump(lr, "model.pkl")
        joblib.dump(dv, "dv.joblib")

        mlflow.log_artifact("model.pkl", artifact_path="models")
        mlflow.log_artifact("dv.joblib", artifact_path="preprocessor")

        # Log model with signature
        signature = infer_signature(X_train, y_train)
        mlflow.sklearn.log_model(lr, artifact_path="sklearn_model", signature=signature, input_example=X_train[:1])

        # Calculate and log model size
        model_size = os.path.getsize("model.pkl")
        mlflow.log_metric("model_size_bytes", model_size)
        print(f"📦 Model size: {model_size} bytes")