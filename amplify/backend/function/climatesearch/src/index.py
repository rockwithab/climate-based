import boto3
import json
import requests

ssm = boto3.client('ssm', region_name='us-east-1')

def get_parameter(name, decrypt=False):
    response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    return response['Parameter']['Value']

def handler(event, context):
    api_key = get_parameter('CustomSearchEngineAPIKey', decrypt=True)
    search_engine_id = get_parameter('CustomSearchEngineId', decrypt=True)

    zip_code = event.get('zip_code', '')
    query = f"climate change resources for zip code {zip_code}"

    search_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"

    response = requests.get(search_url)
    results = response.json()

    search_results = [{
        'title': item['title'],
        'snippet': item['snippet'],
        'link': item['link'],
        # 'image': item['image']
    } for item in results.get('items', [])]

    return {
        'statusCode': 200,
        'body': json.dumps(search_results)
    }