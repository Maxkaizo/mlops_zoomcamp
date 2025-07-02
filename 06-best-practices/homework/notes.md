# Main script test

``` bash
cd ~/mlops_zoomcamp/06-best-practices/homework
python batch.py 2023 3

```

# Run localstack in a docker container

* Install localstack docs: https://docs.localstack.cloud/getting-started/installation/

There are several installation options, but for the homework I'll use docker composer, no persistent storage

``` yaml
services:
  kinesis:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=kinesis
```

* localstack AWS Cli commands example

``` bash
aws --endpoint-url=http://localhost:4566 kinesis list-streams
```

# Create env variables


``` bash
export INPUT_FILE_PATTERN="s3://nyc-duration/in/yellow_tripdata_{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/yellow_tripdata_{year:04d}-{month:02d}.parquet"

export S3_ENDPOINT_URL="http://localhost:4566"
```


# Upload file to localstack S3


``` bash
# make bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
# list buckets
aws --endpoint-url=http://localhost:4566 s3 ls
# list bucket files 
aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration --recursive
# upload a file
aws --endpoint-url=http://localhost:4566 s3 cp yellow_tripdata_2023-03.parquet s3://nyc-duration/in/yellow_tripdata_2023-03.parquet
```



###

``` bash

```
