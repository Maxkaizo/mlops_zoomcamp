import pandas as pd
import argparse
import joblib
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from scipy import sparse

def prepare_features(df):
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', required=True)
    parser.add_argument('--val_path', required=True)
    args = parser.parse_args()

    df_train = pd.read_parquet(args.train_path, engine="pyarrow")
    df_val = pd.read_parquet(args.val_path, engine="pyarrow")

    # Target
    y_train = df_train['duration'].values
    y_val = df_val['duration'].values

    # Features
    dv = DictVectorizer()

    train_dicts = prepare_features(df_train)
    val_dicts = prepare_features(df_val)

    X_train = dv.fit_transform(train_dicts)
    X_val = dv.transform(val_dicts)

    # Save all outputs
    joblib.dump(dv, "dv.pkl")
    sparse.save_npz("X_train.npz", X_train)
    sparse.save_npz("X_val.npz", X_val)
    np.save("y_train.npy", y_train)
    np.save("y_val.npy", y_val)

    print("✅ Vectorization complete and files saved.")