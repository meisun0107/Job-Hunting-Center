import json
import boto3
import csv
import pandas
from numpy import genfromtxt
import numpy

ENDPOINT_NAME = 'kmeans-2022-12-22-02-15-08-492'
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    data = json.loads(json.dumps(event))
    print(data)
    payload = data['data']
    print(payload)
    print(type(payload))
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,ContentType='text/csv',Body=payload)
    result = json.loads(response['Body'].read().decode())
    print(result)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('Post Position Successfully')
    }