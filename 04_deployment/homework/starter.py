import pickle
import pandas as pd
import sys

year = int(sys.argv[1]) # 2021
month = int(sys.argv[2]) # 3

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df
# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-04.parquet
df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)
y_mean = y_pred.mean()
print(f'Mean predicted duration is: {y_mean}')


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred

output_file = f'predictions-{year:04d}-{month:02d}.parquet'


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)



