import requests
from django.shortcuts import render
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def get_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []


def get_repository_contributions(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        contributions = {}
        for repo in repos:
            repo_name = repo['name']
            contrib_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
            contrib_response = requests.get(contrib_url, headers=headers)
            if contrib_response.status_code == 200:
                stats = contrib_response.json()
                for stat in stats:
                    if stat['author']['login'] == username:
                        contributions[repo_name] = stat['total']
        return contributions
    return {}


def portfolio(request):
    username = "sofiahnatiuk"
    activity = get_github_activity(username)
    contributions = get_repository_contributions(username)
    context = {'activity': activity,
               'contributions': contributions,
               }
    return render(request, 'main/portfolio.html', context)


