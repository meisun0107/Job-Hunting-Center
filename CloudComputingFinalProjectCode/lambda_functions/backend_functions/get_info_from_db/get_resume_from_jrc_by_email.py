import json

def lambda_handler(event, context):
    # TODO implement
    
    baseaddress = "https://resume-of-jrc-cloud-computing.s3.amazonaws.com/"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,GET',
            'Access-Control-Allow-Origin': '*'
        },
        'body': baseaddress+event['queryStringParameters']['email']
    }
