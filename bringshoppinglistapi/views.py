from django.http import HttpResponse
import requests
import json
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
load_dotenv()
import os

logger = logging.getLogger('django')

@csrf_exempt
@require_http_methods(["POST"])
def addItem(request):
    logger.info('[START] addItem')
    request_body = json.loads(request.body.decode('utf-8'))
    
    if 'item' not in request_body:
        logger.info('Missing param')
        logger.info('[END] addItem')

        return HttpResponse("Invalid json. Please provide an item.", status=400)
    
    item = request_body['item']
    logger.info('item: ' + item)
    # make request to Bring API
    shopping_list_id = os.getenv('SHOPPING_LIST_ID')
    refresh_token = os.getenv('REFRESH_TOKEN')
    url = f'https://api.getbring.com/rest/v2/bringlists/{shopping_list_id}'

    payload = f'purchase={item}'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Bearer {refresh_token}'
    }

    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code >=200 and response.status_code < 300:
        logger.info('Successful request')
        logger.info('[END] addItem')

        return HttpResponse("Successful response "+response.status_code, status=204)
    else:
        logger.error('Error code: '+response.status_code)
        logger.error(response.text)
        logger.info('[END] addItem')
        return HttpResponse("Error code from API" + response.text, status=200)