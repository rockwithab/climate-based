import json
import requests

def handler(event, context):
    # TODO get these from the parameter store
    api_key = ""
    search_engine_id = ""

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