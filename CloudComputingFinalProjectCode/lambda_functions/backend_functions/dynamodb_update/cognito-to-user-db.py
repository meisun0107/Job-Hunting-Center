import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jrc-users')

def email_verification(useremail):
    ses_client = boto3.client("ses", region_name="us-east-1")
    email_list = ses_client.list_verified_email_addresses()['VerifiedEmailAddresses']
    if useremail not in email_list:
        response = ses_client.verify_email_identity(EmailAddress=useremail)
    return

# example event = 
# {'version': '1', 'region': 'us-east-1', 'userPoolId': 'us-east-1_sJ9EEEEEE', 
# 'userName': '1d3e62b0-1dc6-4fed-9872-b67bfaaaaaa', 
# 'callerContext': {'awsSdkVersion': 'aws-sdk-unknown-unknown', 'clientId': '7bead3niq15471jo3eeeeeee'}, 
# 'triggerSource': 'PostConfirmation_ConfirmSignUp', 
# 'request': {'userAttributes': {'sub': '1d3e62b0-1dc6-4fed-9872-b67bf9gggggg', 'email_verified': 'true', 
# 'cognito:user_status': 'CONFIRMED', 'cognito:email_alias': 'abc@gmail.com', 'email': 'abc@gmail.com'}}, 'response': {}}


def lambda_handler(event, context):
    print(event)
    logger.debug("---------------------")
    logger.debug(event)
    logger.debug("++++++++++++++++++++++")
    # TODO implement
    preferred_username = event['request']['userAttributes']['preferred_username']
    x = preferred_username.split(",")
    username = x[0]
    user_tag = 'user'
    if len(x) == 2:
        user_tag = x[1]
    if user_tag != 'company':
        user_tag = 'user'
    useremail = event['request']['userAttributes']['email']
    password = "123abc"
    data = dict()
    data['email'] = useremail
    data['username'] = username
    # data['password'] = password
    data['user_tag'] = user_tag
    # data['user_tag2'] = 'random shit'
    
    email_verification(useremail)
    
    response = table.put_item(Item=data)
    return event