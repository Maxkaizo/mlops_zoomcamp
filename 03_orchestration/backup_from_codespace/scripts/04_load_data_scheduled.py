import pandas as pd
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import urllib.error

def read_dataframe(year, month):
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet'
    try:
        df = pd.read_parquet(url)
    except (urllib.error.HTTPError, FileNotFoundError) as e:
        raise RuntimeError(f"❌ No se pudo cargar {url}: {e}")

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    df[['PULocationID', 'DOLocationID']] = df[['PULocationID', 'DOLocationID']].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exec_date", required=False)
    args = parser.parse_args()

    if args.exec_date:
        today = datetime.strptime(args.exec_date, "%Y-%m-%d")
    else:
        today = datetime.today()

    print(f"🧪 Fecha de ejecución usada: {today.strftime('%Y-%m-%d')}")

    train_date = today - relativedelta(months=2)
    val_date = today - relativedelta(months=1)

    df_train = read_dataframe(train_date.year, train_date.month)
    df_val = read_dataframe(val_date.year, val_date.month)

    df_train.to_parquet("df_train.parquet")
    df_val.to_parquet("df_val.parquet")

    print("✅ Archivos guardados: df_train.parquet, df_val.parquet")