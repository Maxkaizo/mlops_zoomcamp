#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:


get_ipython().system('python -V')


# In[4]:


import pickle
import pandas as pd


# In[6]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[7]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


# In[9]:


df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')


# In[10]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[11]:


y_pred.std()


# In[14]:


year = 2023
month = 3


# In[15]:


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[16]:


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred


# In[20]:


output_file = f'predictions-{year:04d}-{month:02d}.parquet'


# In[21]:


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[22]:


get_ipython().system(' ls -lash *.parquet')


# In[ ]:




