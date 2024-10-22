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
    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos_response = requests.get(repos_url, headers=headers)

    if repos_response.status_code == 200:
        repos = repos_response.json()
        contributions = {}
        for repo in repos:
            repo_name = repo['name']
            contributions[repo_name] = {
                'commit_count': 0,
                'commit_messages': []
            }
            contrib_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
            contrib_response = requests.get(contrib_url, headers=headers)

            if contrib_response.status_code == 200:
                stats = contrib_response.json()
                for stat in stats:
                    if stat['author']['login'] == username:
                        contributions[repo_name]['commit_count'] = stat['total']
                        break

            commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
            commits_response = requests.get(commits_url, headers=headers)

            if commits_response.status_code == 200:
                commits = commits_response.json()
                for commit in commits:
                    contributions[repo_name]['commit_messages'].append(commit['commit']['message'])

            if contributions[repo_name]['commit_count'] == 0:
                contributions[repo_name]['commit_count'] = 0

        return contributions
    else:
        print(f"Failed to fetch repositories: {repos_response.status_code} - {repos_response.text}")
        return {}


def portfolio(request):
    username = "sofiahnatiuk"
    activity = get_github_activity(username)
    contributions = get_repository_contributions(username)
    context = {'activity': activity,
               'contributions': contributions,
               }
    return render(request, 'main/portfolio.html', context)


