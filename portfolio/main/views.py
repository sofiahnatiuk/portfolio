import requests
from django.shortcuts import render
import os
from datetime import datetime


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def get_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events = response.json()

        for event in events:
            created_at_iso = event['created_at']
            created_at_readable = datetime.fromisoformat(created_at_iso[:-1]).strftime('%B %d, %Y, %I:%M %p')
            event['created_at'] = created_at_readable

        return events
    else:
        return []


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

            commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
            commits_response = requests.get(commits_url, headers=headers)

            if commits_response.status_code == 200:
                commits = commits_response.json()
                contributions[repo_name]['commit_count'] = len(commits)  # Count total commits

                for commit in commits:
                    message = commit['commit']['message']
                    date_iso = commit['commit']['committer']['date']

                    date_readable = datetime.fromisoformat(date_iso[:-1]).strftime('%B %d, %Y, %I:%M %p')

                    contributions[repo_name]['commit_messages'].append((date_readable, message))

                contributions[repo_name]['commit_messages'].sort(key=lambda x: x[0], reverse=True)

            else:
                print(
                    f"Failed to fetch commits for {repo_name}: {commits_response.status_code} - {commits_response.text}")

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


