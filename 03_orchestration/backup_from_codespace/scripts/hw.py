import pandas as pd
import argparse

def read_dataframe(year, month):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    df = pd.read_parquet(url)

    print('before filtering')
    size_before = len(df)
    print(f"size before: {size_before}")

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    print('after filtering')
    size_after = len(df)
    print(f"size after: {size_after}")

    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    args = parser.parse_args()

    print(f"Loading training data for {args.year}-{args.month:02d}")
    df_train = read_dataframe(args.year, args.month)

    df_train.to_parquet("df_train.parquet")

    print("✅ Data saved as 'df_train.parquet'.")