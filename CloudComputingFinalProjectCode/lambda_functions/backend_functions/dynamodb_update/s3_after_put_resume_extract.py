import json
import boto3

def insert(username, resume_keywords):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('jrc-users')
    response = table.update_item(
        Key={'email': username},
        UpdateExpression="set keywords=:r",
        ExpressionAttributeValues={
            ':r': resume_keywords},
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    return

def lambda_handler(event, context):
    records = [x for x in event.get('Records', []) if x.get('eventName') == 'ObjectCreated:Put']
    sorted_events = sorted(records, key=lambda e: e.get('eventTime'))
    latest_event = sorted_events[-1] if sorted_events else {}
    info = latest_event.get('s3', {})
    print(info)
    file_key = info.get('object', {}).get('key')
    index = file_key.find("%40")
    new_file_key = file_key[:index]+'@'+file_key[index+3:]
    
    bucket_name = info.get('bucket', {}).get('name')
    print("Before Textract "+new_file_key+" "+bucket_name)
    client = boto3.client('textract')
    # images = convert_from_path(bucket_name+'/'+filekey)
    response = client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': new_file_key
            }
        }
    )
    
    resume_keywords = ''
    blocks=response['Blocks']
    for block in blocks:
        if block['BlockType'] == 'LINE':
            resume_keywords += (block['Text'] + ' ')
    print(resume_keywords)
    
    insert(new_file_key, resume_keywords)
            
    # print(blocks)
    return {
        'statusCode': 200,
        'body': json.dumps('s3_put_extract_success!')
    }