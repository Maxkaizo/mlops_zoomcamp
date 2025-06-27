import requests

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49664349626995788546610880530340811045745011354364805122",
                "data": "ewogICAgInJpZGUiOiB7CiAgICAgICAgIlBVTG9jYXRpb25JRCI6IDEzMCwKICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgfSwgCiAgICAicmlkZV9pZCI6IDE1Ngp9",
                "approximateArrivalTimestamp": 1750203556.452
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49664349626995788546610880530340811045745011354364805122",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::438480637738:role/lambda-kinesis-role",
            "awsRegion": "us-west-1",
            "eventSourceARN": "arn:aws:kinesis:us-west-1:438480637738:stream/ride_events_calif"
        }
    ]
}


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(url, json=event)
print(response.json())