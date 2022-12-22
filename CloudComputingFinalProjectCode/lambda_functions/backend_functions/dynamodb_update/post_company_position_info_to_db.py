import json
import boto3
from boto3.dynamodb.conditions import Key
import string
import logging
import requests

ENDPOINT_NAME = "kmeans-2022-12-22-17-57-42-370"
runtime = boto3.client('runtime.sagemaker')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def getKeyWordList(job_description):
    # Split the string into a list of words
    words = job_description.split(' ')

    # Remove any non-alphabetic characters from the list
    words = [word for word in words if word.isalpha()]
    
    # Remove copula from the string
    # copula = ["stop", "the", "to", "and", "a", "in", "it", "is", "I", "that", "had", "on", "for", "were", "was", "of", "by", "will", "with"]
    stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    # software_engineer_words = ["agile", "algorithm", "API", "application", "architecture", "backend", "bug", "C", "C++", "C#", "cloud", "code", "coding", "compiler", "computer", "data", "database", "debugging", "development", "digital", "electronic", "engineer", "engineering", "frontend", "function", "graphic", "HTML", "interface", "Java", "JavaScript", "machine", "management", "manipulation", "mathematics", "matrix", "method", "mobile", "object", "operating", "optimization", "parameter", "performance", "PHP", "platform", "program", "programming", "Python", "query", "real-time", "refactoring", "release", "security", "server", "solution", "sorting", "SQL", "structure", "support", "system", "testing", "tool", "user", "UX", "validation", "web", "web application", "web development", "webpage", "XML", "adaptability", "analytical", "collaboration", "communication", "creativity", "flexibility", "leadership", "organizational", "problem-solving", "teamwork", "time management", "cloud computing", "distributed systems", "information technology", "machine learning", "object-oriented", "software development", "software engineering", "systems analysis", "technical", "technical writing", "client-server", "communication skills", "data structures", "database design", "debugging skills", "design patterns", "development experience", "familiarity with", "hardware", "information systems", "internet", "interpersonal", "intranet", "language", "logic", "management skills", "mathematical", "mobile development", "multithreading", "networking", "operating systems", "organization", "performance optimization", "programming languages", "protocols", "quality assurance", "refactoring skills", "scripting", "security protocols", "server-side", "source control", "systems design", "technical expertise", "technical skills", "testing experience", "user experience", "version control", "web development skills", "web services","web services", "web-based", "webpage design", "XML", "XML parsing", "XML schema", "YAML", "zip", "zipping", "web application security", "web application testing", "web development frameworks", "web development skills", "web services development", "web services testing", "webpage design skills", "XML parsing skills", "XML schema design", "YAML skills", "zip skills", "zipping skills", "web application security skills", "web application testing skills", "web development frameworks experience", "web services development skills", "web services testing skills", "webpage design experience", "XML parsing experience", "XML schema design skills", "YAML experience", "zip experience", "zipping experience"]

    words = [word.lower() for word in words if word.lower() not in stop_words]
    # words = [word for word in words if word.lower() in software_engineer_words]

    # Join the words back into a single string
    cleaned_string = ' '.join(words)

    # Create a translation table to remove punctuation and digits
    translator = str.maketrans('', '', string.punctuation + string.digits)

    # Use the translate method to remove the punctuation and digits
    cleaned_string = cleaned_string.translate(translator)

    return cleaned_string.split(' ')

def putDescription2ElasticSearch(company_email, positionid, position_description):
    host = 'https://search-test-nmxqoeiq77vratgyuazxgtyecy.us-east-1.es.amazonaws.com/'
    path = 'jobs/_doc/'
    url = host + path
    payload = {'jid': company_email + '-' + positionid , 'description': position_description}
    r = requests.post(url, auth = ('test', 'Zhangwenyuan666!'), json = payload)
    logger.debug("----------putDescription2ElasticSearch-----------")
    logger.debug(r.text)
    logger.debug("+++++++++++putDescription2ElasticSearch+++++++++++")
    

def lambda_handler(event, context):
    print(event)
    # TODO implement
    client = boto3.resource('dynamodb')
    table = client.Table('company_positions')
    skillset = client.Table('SkillSet')
    print(event['queryStringParameters']['email'])
    print(event['queryStringParameters']['position_name'])
    print(event['queryStringParameters']['position_description'])
    company_email = event['queryStringParameters']['email']
    positionid = event['queryStringParameters']['position_name']
    position_description = event['queryStringParameters']['position_description']
    
    putDescription2ElasticSearch(company_email, positionid, position_description)
    
    wordlist = getKeyWordList(position_description)
    
    serverwordlist = skillset.scan()['Items'][0]['SkillSet']
    print(len(serverwordlist))
    cluster = get_cluster_from_old_configuration(wordlist, serverwordlist)
    
    print(wordlist)
    print(cluster)
    
    new_item = {
        "company_email": company_email,
        "positionid": positionid,
        "position_description": position_description,
        "wordlist": wordlist,
        "used_for_training": False,
        "cluster": cluster
    }

    result = table.put_item(Item=new_item)
    print(result)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('Post Position Successfully and the cluster is '+str(cluster))
    }

def get_cluster_from_old_configuration(wordlist, serverwordlist):
    worddict = wordlist_to_worddict(serverwordlist)
    dictlength = len(worddict)
    print(dictlength)
    vec = [0]*dictlength
    for word in wordlist:
        print(type(worddict))
        print(worddict)
        if word in worddict:
            index = worddict[word]
            if vec[index] == 0:
                vec[index] = 5
            else:
                vec[index] = vec[index] + 1
    payload = ','.join(map(str, vec))
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,ContentType='text/csv',Body=payload)
    cluster = int(json.loads(response['Body'].read().decode())['predictions'][0]['closest_cluster'])
    print("new position cluster number is:")
    print(cluster)
    return cluster
    

def wordlist_to_worddict(wordlist):
    worddict = {}
    for i in range(len(wordlist)):
        worddict[wordlist[i]] = i
        
    return worddict