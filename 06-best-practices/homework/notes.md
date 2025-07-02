

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

* an example command to show kinesis streams

``` bash
aws --endpoint-url=http://localhost:4566 kinesis list-streams
```


###

``` bash

```
