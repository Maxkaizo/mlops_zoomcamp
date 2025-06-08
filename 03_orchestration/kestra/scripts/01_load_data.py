import pandas as pd
import argparse

def read_dataframe(year, month):
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet'
    df = pd.read_parquet(url)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    return df

def next_month_and_year(year, month):
    month = int(month)
    year = int(year)
    if month == 12:
        return year + 1, 1
    else:
        return year, month + 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    args = parser.parse_args()

    print(f"Loading training data for {args.year}-{args.month:02d}")
    df_train = read_dataframe(args.year, args.month)

    val_year, val_month = next_month_and_year(args.year, args.month)
    print(f"Loading validation data for {val_year}-{val_month:02d}")
    df_val = read_dataframe(val_year, val_month)

    df_train.to_parquet("df_train.parquet")
    df_val.to_parquet("df_val.parquet")

    print("✅ Data saved as 'df_train.parquet' and 'df_val.parquet'.")
