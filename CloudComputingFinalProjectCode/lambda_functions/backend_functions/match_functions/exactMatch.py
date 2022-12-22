import json
import boto3
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def readUserDBWordlist(user_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('jrc-users')
    user_details = table.get_item(Key={'email': user_email})['Item']
    keywords = user_details["keywords"]
    return keywords.split(' ')

def readUserDB(user_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('jrc-users')
    user_details = table.get_item(Key={'email': user_email})['Item']
    logger.debug("----------user_details-----------")
    logger.debug(user_details)
    logger.debug("+++++++++++user_details+++++++++++")
    return user_details["keywords"]
    
def getPositions(longWordString):
    # to do
    baseUrl = 'https://search-test-nmxqoeiq77vratgyuazxgtyecy.us-east-1.es.amazonaws.com/'
    auth = ('test', 'Zhangwenyuan666!')
    
    headers = {'Content-Type': 'application/json'}
    query = {
        "size": 200,
        "query": {
            "match": {
                "description": longWordString
            }
        }
    }
    path = 'jobs/_search'
    url = baseUrl + path
    response = requests.get(url, auth=auth, headers=headers, data=json.dumps(query))
    logger.debug("----------getPositions-----------")
    logger.debug(response)
    logger.debug(json.loads(response.text))
    logger.debug("+++++++++++getPositions+++++++++++")
    return json.loads(response.text)

def getTopMatchJobDescription(num, jds):
    jd_size = int(jds['hits']['total']['value'])
    num = min(num, jd_size)
    hits = jds['hits']['hits']
    ans = []
    for i in range(num):
        data = dict()
        data['order'] = i + 1
        data['company_email'] = hits[i]['_source']['jid'].split('-')[0]
        data['positionid'] = hits[i]['_source']['jid'].split('-')[1]
        data['job_description'] = hits[i]['_source']['description']
        ans.append(data)
    logger.debug("----------getTopMatchJobDescription-----------")
    logger.debug(ans)
    logger.debug("+++++++++++getTopMatchJobDescription+++++++++++")
    return ans


def sendEmailToUser(Data, email):
    ses_client = boto3.client("ses", region_name="us-east-1")
    if len(Data) < 3:
        logger.debug("----------too few job recommendation-----------")
        logger.debug("+++++++++++too few job recommendation+++++++++++")
        return
    
    message = 'Thank you for waiting, after careful research, Here is my job recommendation: \n1.\nCompany email: {}\nPosition title: {}\nJob Description: {} \n2.\nCompany email: {}\nPosition title: {}\nJob Description: {}\n3.\nCompany email: {}\nPosition title: {}\nJob Description: {}\n\nGood luck' \
        .format(Data[0]['company_email'], Data[0]['positionid'], Data[0]['job_description'],Data[1]['company_email'], Data[1]['positionid'], Data[1]['job_description'],Data[2]['company_email'], Data[2]['positionid'], Data[2]['job_description'])
    
    ses_client = boto3.client("ses", region_name="us-east-1")
    email_list = ses_client.list_verified_email_addresses()['VerifiedEmailAddresses']
    if email not in email_list:
        response = ses_client.verify_email_identity(EmailAddress=email)
        return

    
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": message,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Your job recommendation is ready!",
            },
        },
        Source="waynezhang226@gmail.com",
    )
    return response

def lambda_handler(event, context):
    # TODO implement
    logger.debug("----------event-----------")
    logger.debug(event)
    logger.debug("+++++++++++event+++++++++++")
    
    user_email = event['queryStringParameters']['matchemail']
    longWordString = readUserDB(user_email)
    jds = getPositions(longWordString)
    lists = getTopMatchJobDescription(3, jds)
    # sendEmailToUser(lists, user_email)
    print(lists)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(lists)
    }
