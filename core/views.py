import json
import os

import requests
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User


# Create your views here.
@api_view(['GET'])
def home_view(request):
    return Response({"success": True, "message": "Log in to api."})


@api_view(['GET'])
def get_repos(request):
    authorization_header = request.headers.get('authorization')

    if authorization_header:
        token = authorization_header.split(' ')[1]
        db_user = User.objects.filter(access_token=token)

        if db_user.exists():
            user = db_user.first()

            response = requests.get(
                f'https://api.github.com/users/{user.username}/repos',
                headers={'Authorization': f'token {token}'}
            )

            repos = response.json()

            return Response({"success": True, "repos": repos})
        return Response({"success": False, "message": "Account was not recognized. Please sign in."})
    return Response({"success": False, "message": "This route is protected. Please sign in."})


@api_view(['GET'])
def get_commits(request):
    authorization_header = request.headers.get('authorization')

    if authorization_header:
        token = authorization_header.split(' ')[1]
        db_user = User.objects.filter(access_token=token)

        if db_user.exists():
            repo_name = request.query_params.get('repo_name')
            user = db_user.first()

            response = requests.get(
                f'https://api.github.com/repos/{user.username}/{repo_name}/commits',
                headers={'Authorization': f'token {token}'}
            )

            repos = response.json()

            return Response({"success": True, "commits": repos})
        return Response({"success": False, "message": "Account was not recognized. Please sign in again."})
    return Response({"success": False, "message": "This route is protected. Please sign in."})


@api_view(['GET'])
def get_commit(request):
    authorization_header = request.headers.get('authorization')

    if authorization_header:
        token = authorization_header.split(' ')[1]
        db_user = User.objects.filter(access_token=token)

        if db_user.exists():
            repo_name = request.query_params.get('repo_name')
            commit_sha = request.query_params.get('commit_sha')
            user = db_user.first()

            print({"commit_sha": commit_sha, "repo_name": repo_name})

            # https://api.github.com/repos/gabrielteodosio/github-api-consumer/git/commits/3366f14e7132ca25bb77c4f2084888b515568fe8
            response = requests.get(
                f'https://api.github.com/repos/{user.username}/{repo_name}/git/commits/{commit_sha}',
                headers={'Authorization': f'token {token}'}
            )

            repos = response.json()

            return Response({"success": True, "commits": repos})
        return Response({"success": False, "message": "Account was not recognized. Please sign in again."})
    return Response({"success": False, "message": "This route is protected. Please sign in."})


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

    response = requests.get('https://api.github.com/user', headers={'Authorization': f'token {token}'})
    github_user_data = response.json()

    db_user = User.objects.filter(username=github_user_data.get('login'))

    if db_user.exists():
        db_user.update(
            access_token=token,
            name=github_user_data.get('name'),
            email=github_user_data.get('email'),
            username=github_user_data.get('login'),
            avatar_url=github_user_data.get('avatar_url')
        )

        user = db_user.first()
    else:
        user = User.objects.create(
            access_token=token,
            name=github_user_data.get('name'),
            email=github_user_data.get('email'),
            username=github_user_data.get('login'),
            avatar_url=github_user_data.get('avatar_url')
        )

    user.save()

    app_url = os.environ.get('APP_URL')
    if not app_url:
        app_url = 'http://localhost:8080/app'

    redirect_url = f'{app_url}'

    response = HttpResponseRedirect(redirect_to=redirect_url)
    response.set_cookie('gh_access_token', token)

    return response
