from django.http import HttpResponse
import requests
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
load_dotenv()
import os

@csrf_exempt
@require_http_methods(["POST"])
def addItem(request):

    request_body = json.loads(request.body.decode('utf-8'))
    
    if 'item' not in request_body:
        return HttpResponse("Invalid json. Please provide an item.", status=400)
    
    item = request_body['item']
    # make request to Bring API
    shopping_list_id = os.getenv('SHOPPING_LIST_ID')
    refresh_token = os.getenv('REFRESH_TOKEN')
    url = f'https://api.getbring.com/rest/v2/bringlists/{shopping_list_id}'

    payload = f'purchase={item}'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Bearer {refresh_token}'
    }

    resonse = requests.request("PUT", url, data=payload, headers=headers)
    return HttpResponse(status=204)