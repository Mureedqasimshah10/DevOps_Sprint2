import boto3
import json
import os
# Creating the client for DynamoDB
tablename = os.environ["Alarm_key"]
dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    # Alarm information in JSON Format
    # Prase informaton to put in the DynamoDB
    for record in event['Records']:
        # Prase message key value from string to json
        message = json.loads(record['Sns']['Message'])
        item = {
            "AlarmName": {'S': message["AlarmName"]},
            "NewStateReason": {'S': message["NewStateReason"]},
            "Region": {'S': message['Region']},
            "MetricName": {'S': message["Trigger"]["MetricName"]},
            "URL": {'S': message["Trigger"]["Dimensions"][0]["value"]}
        }
        # Putting item in the DynamoDB Table
        response = dynamodb.put_item(
            TableName = tablename,
            Item = item
        )
    print(event)
    return response