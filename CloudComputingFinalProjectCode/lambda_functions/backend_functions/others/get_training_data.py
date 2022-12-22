import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    bucket = 'ui-of-jrc-cloud-computing'
    key = 'training_data.csv'
    client = boto3.resource('dynamodb')
    table = client.Table('company_positions')
    skillset = client.Table('SkillSet')
    
    response = table.scan()
    items = response['Items']
    # Get word dictionary
    wordindex = static_words(table, skillset, items)
    
    #  Create training data
    data = create_training_data(wordindex, items)
    print(data)
    
    flag = write_into_training_data_csv(data, bucket, key)
    
    returnSentence = ""
    if flag:
        returnSentence = "Get Training Data Successfully!"
    else:
        returnSentence = "Get Training Data Failed!"
        
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(returnSentence)
    }

def create_training_data(wordindex, items):
    dictlength = len(wordindex)
    data = []
    for item in items:
        if item.get('wordlist'):
            vec = [0]*dictlength
            for word in item['wordlist']:
                index = wordindex[word]
                if vec[index] == 0:
                    vec[index] = 5
                else:
                    vec[index] = vec[index] + 1
            data.append(vec)
    print("positionsize")
    print(len(data))
    return data


def static_words(table, skillset, items):
    wordlist = []
    wordset = set()
    wordindex = {}
    index = 0
    for item in items:
        if item.get('wordlist'):
            if not (item.get('used_for_training') and item['used_for_training'] == True):
                item['used_for_training'] = True
                table.put_item(Item=item)
            for word in item["wordlist"]:
                if word in wordset:
                    continue
                else:
                    wordlist.append(word)
                    wordset.add(word)
                    wordindex[word] = index
                    index = index+1
        else:
            if item.get('used_for_training') and item['used_for_training'] == True:
                item['used_for_training'] = False
                table.put_item(Item=item)
    item = {
        "Name": "skillSet",
        "SkillSet": wordlist
    }
    skillset.put_item(Item=item)
    print("worddictsize")
    print(len(wordindex))
    return wordindex
    

def write_into_training_data_csv(data, bucket, key):
    # Convert the data to a CSV string
    csv_str = '\n'.join([','.join(map(str, row)) for row in data])
    print("csv")
    print(csv_str)
    # Use the Boto3 client to write the CSV string to the specified S3 bucket and key
    s3 = boto3.client('s3')
    s3.put_object(Body=csv_str, Bucket=bucket, Key=key)
    return True
