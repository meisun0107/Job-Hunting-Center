import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def check_user_exist(email):
    # queryDynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('jrc-users')
    response = table.get_item(Key={'email': email})
    if 'Item' in response:
        return True
    else:
        return False


def lambda_handler(event, context):
    # TODO implement
    logger.debug("---------------------")
    logger.debug(event)
    logger.debug("++++++++++++++++++++++")
    email = event['queryStringParameters']['email']
    username = event['queryStringParameters']['username']
    password = event['queryStringParameters']['password']
    user_tag = event['queryStringParameters']['tag']
    
    if check_user_exist(email):
        return {
            'statusCode': 200,
            'body': json.dumps('User already exists!')
        }
    
    # if user not exist
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('jrc-users')
    data = dict()
    data['email'] = email
    data['username'] = username
    data['password'] = password
    data['user_tag'] = user_tag
    
    response = table.put_item(Item=data)
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('User register successfully')
    }
