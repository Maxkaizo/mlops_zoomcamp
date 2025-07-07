import argparse
import joblib
import numpy as np
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error
import mlflow
from scipy import sparse
from mlflow.models.signature import infer_signature

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mlflow_uri", required=True)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--train_path", required=True)
    parser.add_argument("--train_target", required=True)
    parser.add_argument("--val_path", required=True)
    parser.add_argument("--val_target", required=True)
    parser.add_argument("--dv_path", required=True)
    args = parser.parse_args()

    # MLflow config
    mlflow.set_tracking_uri(args.mlflow_uri)
    mlflow.set_experiment(args.experiment)

    # Load features and target
    X_train = sparse.load_npz(args.train_path)
    X_val = sparse.load_npz(args.val_path)
    y_train = np.load(args.train_target)
    y_val = np.load(args.val_target)
    dv = joblib.load(args.dv_path)

    with mlflow.start_run():
        print("📍 Run ID:", mlflow.active_run().info.run_id)
        print("📍 Artifact URI:", mlflow.get_artifact_uri())
        # Prepare data for XGBoost
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)

        # Training params
        params = {
            "max_depth": 6,
            "learning_rate": 0.1,
            "objective": "reg:squarederror",
            "nthread": 4,
            "seed": 42
        }

        mlflow.log_params(params)

        # Train
        booster = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=100,
            evals=[(dval, "validation")],
            early_stopping_rounds=20
        )

        # Evaluate
        y_pred = booster.predict(dval)
        rmse = root_mean_squared_error(y_val, y_pred)
        mlflow.log_metric("rmse", rmse)

        input_example = X_train[:1].toarray().astype("float32")
        signature = infer_signature(X_train.toarray(), y_train)

        # Save and log artifacts
        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow",input_example=input_example, signature=signature)
        booster.save_model("model.json")
        joblib.dump(dv, "dv_logged.pkl")
        mlflow.log_artifact("dv_logged.pkl", artifact_path="preprocessor")

        with open("artifact_check.txt", "w") as f:
          f.write("Hello from Kestra task!")
        mlflow.log_artifact("artifact_check.txt")