import json
import os

import requests
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def home_view(request):
    return Response({"success": True})


@api_view(['GET'])
def authorize(request):
    url = 'https://github.com/login/oauth/access_token'

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    body = {
        "code": request.query_params.get("code"),
        "client_id": os.environ.get('GH_CLIENT_ID') or "Iv1.a77100850ebb1d4d",
        "client_secret": os.environ.get('GH_CLIENT_SECRET') or "08d0d612b00bf13feff11e6e0dafaff82844ce6d",
    }

    response = requests.post(url, data=json.dumps(body), headers=headers)
    token = response.json().get('access_token')

    app_url = os.environ.get('APP_URL')
    if not app_url:
        app_url = 'http://localhost:8080/app'

    redirect_url = f'{app_url}?access_token={token}'

    return HttpResponseRedirect(redirect_to=redirect_url)
