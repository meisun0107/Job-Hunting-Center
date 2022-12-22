import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

from decimal import Decimal
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    # TODO implement
    client = boto3.resource('dynamodb')
    table = client.Table('jrc-users')
    
    if not event.get('queryStringParameters') or not event['queryStringParameters'].get('email'):
        return {
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps("No email")
    }
    
    response = table.get_item(
        Key={
            'email': event['queryStringParameters']['email']
        }
    )
    print(response['Item'])
    
    user_tag = "no Tag"
    
    if "user_tag" in response['Item']:
        user_tag =  response['Item']['user_tag']
    
    jobs_table = client.Table('company_positions')
    jobs=[]
    
    jobs = jobs_table.query(
        KeyConditionExpression =
        Key('company_email').eq(response['Item']['email'])
    ) 
    # logger.debug("---------------jobs---------------")
    # logger.debug(jobs)
    # logger.debug("---------------jobs---------------")
    for item in jobs['Items']:
        item['cluster'] = str(item['cluster'])
    # print("HEre is ")
    # print(response['Item'])
    profileObject = {}
    profileObject['email'] = response['Item']['email']
    if response['Item'].get('username'):
        profileObject['username']= response['Item']['username'],
    if response['Item'].get('user_tag'):
        profileObject['user_tag']= user_tag.lower(),
    profileObject['jobs'] = jobs['Items']
    
    # print(profileObject['jobs'])
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
