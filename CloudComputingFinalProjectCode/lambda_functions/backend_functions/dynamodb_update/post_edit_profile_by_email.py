import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # TODO implement
    client = boto3.resource('dynamodb')
    table = client.Table('jrc-users')
    response = table.get_item(
        Key={
            'email': event['queryStringParameters']['email']
        }
    )
    print(response['Item'])
    response['Item']['username'] = event['queryStringParameters']['username']
    if event['queryStringParameters']['user_tag'].lower() == "company":
        response['Item']['user_tag'] = "company"
    else:
        response['Item']['user_tag'] = "user"
        
    table.put_item(Item=response['Item'])
    
    response = table.get_item(
        Key={
            'email': event['queryStringParameters']['email']
        }
    )
    
    profileObject = {
        'email': response['Item']['email'],
        'username': response['Item']['username'],
        'user_tag': response['Item']['user_tag']
    }
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(profileObject)
    }
