import json
import boto3
import math
import random
from boto3.dynamodb.conditions import Key

cluster_number = 5

def lambda_handler(event, context):
    # TODO implement
    
    email = event['queryStringParameters']['email']
    client = boto3.resource('dynamodb')
    usertable = client.Table('jrc-users')
    positiontable = client.Table('company_positions')
    skillset = client.Table('SkillSet')
    
    skillsetwords = skillset.scan()['Items'][0]['SkillSet']
    items = positiontable.scan()['Items']
    # random.shuffle(items)
    positions_info = get_position_representive_from_clusters(items, cluster_number)
    
    userinfo_response = usertable.get_item(
        Key={
            'email':email
        }
    )
    userinfo = userinfo_response['Item']
    user_resume_key_words = get_user_resume_key_words_list(userinfo['keywords'])
    
    cluster = get_closest_cluster_number(positions_info, user_resume_key_words, skillsetwords)

    returnlist = filter_positions_by_cluster(items, cluster)
    # random.shuffle(returnlist)
    
    print(json.dumps(returnlist))
    print(type(json.dumps(returnlist)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(returnlist)
    }

def get_user_resume_key_words_list(keywords):
    splited_keywords = keywords.split(' ')
    return splited_keywords
    

def get_position_representive_from_clusters(items, cluster_number):
    position_info = []
    
    indexset = set([-1])
    for item in items:
        if not item['cluster'] in indexset:
            pos_keys = item['wordlist']
            position_info.append(pos_keys)
            indexset.add(item['cluster'])

    return position_info


def get_closest_cluster_number(positions_info, user_resume_key_words, skillsetwords):
    worddict = wordlist_to_worddict(skillsetwords)
    position_data = []
    for position in positions_info:
        positiondatatemp = get_data_from_wordlist(position, worddict)
        position_data.append(positiondatatemp)
    user_resume_data = get_data_from_wordlist(user_resume_key_words, worddict)
    distance = get_distance(user_resume_data, position_data)
    cluster = 0
    min_distance = distance[0]
    for i in range(len(distance)):
        print("distance is: " + str(distance[i]) +"index is: "+str(i) )
        if min_distance > distance[i]:
            cluster = i
            min_distance = distance[i]
    print("cluster is: "+str(cluster))
    return cluster
    

def get_data_from_wordlist(wordlist, worddict):
    dictlength = len(worddict)
    vec = [0]*dictlength
    for word in wordlist:
        if worddict.get(word):
            index = worddict[word]
            if vec[index] == 0:
                vec[index] = 5
            else:
                vec[index] = vec[index] + 1
    return vec
    
    
def wordlist_to_worddict(wordlist):
    worddict = {}
    for i in range(len(wordlist)):
        worddict[wordlist[i]] = i
        
    return worddict


def get_distance(wordlistmain, wordlistcompare):
    distance = []
    
    for wordlist in wordlistcompare:
        sum = 0
        count = 0
        for i in range(len(wordlistmain)):
            if wordlist[i] == 0:
                continue
            else:
                count = count + 1
                sum = sum + (wordlistmain[i]-wordlist[i])**2
        sum = sum * (len(wordlistmain) / count)
        sum = math.sqrt(sum)
        distance.append(sum)
    print(distance)
    return distance


def filter_positions_by_cluster(items, cluster):
    returnlist = []
    count = 0
    print("filter_positions_by_cluster: "+str(cluster))
    for item in items:
        print('cluster number of '+str(item['company_email']) + str(item['positionid']) + ' is '+str(item['cluster']))
        if item['cluster'] == cluster:
            data = {}
            data['company_email'] = item['company_email']
            data['positionid'] = item['positionid']
            data['position_description'] = item['position_description']
            returnlist.append(data)
            count= count + 1
            if count >= 10:
                break
    return returnlist