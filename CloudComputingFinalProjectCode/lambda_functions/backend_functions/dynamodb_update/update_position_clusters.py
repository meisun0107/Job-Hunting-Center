import json
import boto3

ENDPOINT_NAME = "kmeans-2022-12-22-19-09-32-208"
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    # TODO implement
    client = boto3.resource('dynamodb')
    table = client.Table('company_positions')
    skillset = client.Table('SkillSet')
    
    
    
    wordlist2 = skillset.scan()['Items']
    print(wordlist2)
    wordlist1 = wordlist2[0]
    print("wordlist1")
    print(wordlist1)
    wordlist = wordlist1['SkillSet']
    response = table.scan()
    items = response['Items']
    print(len(wordlist))
    worddict = wordlist_to_worddict(wordlist)
    
    #  Update clustering data
    flag = update_cluster_info(worddict, items, table)
    
    returnSentence = ""
    if flag:
        returnSentence = "Update Clustering Successfully!"
    else:
        returnSentence = "Update Clustering Failed!"
        
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

def update_cluster_info(worddict, items, table):
    dictlength = len(worddict)
    data = []
    for item in items:
        result = -1
        if item.get('wordlist'):
            vec = [0]*dictlength
            for word in item['wordlist']:
                if worddict.get(word):
                    index = worddict[word]
                    if vec[index] == 0:
                        vec[index] = 5
                    else:
                        vec[index] = vec[index] + 1
            payload = ','.join(map(str, vec))
            print(payload)
            response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,ContentType='text/csv',Body=payload)
            result = int(json.loads(response['Body'].read().decode())['predictions'][0]['closest_cluster'])
            print(result)
        item['cluster'] = result
        table.put_item(Item=item)
    return True

def wordlist_to_worddict(wordlist):
    worddict = {}
    for i in range(len(wordlist)):
        worddict[wordlist[i]] = i
    return worddict