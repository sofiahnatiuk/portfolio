import requests
from django.shortcuts import render
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def get_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []


def portfolio(request):
    username = "sofiahnatiuk"
    activity = get_github_activity(username)
    context = {'activity': activity}
    return render(request, 'main/portfolio.html', context)