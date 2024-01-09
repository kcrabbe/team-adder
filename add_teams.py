import requests
import json
import os
import csv
from datetime import datetime

# Run script
# python3 add_teams.py

CONST_ORG = 'fanduel'
CONST_TEAM = 'racing'
CONST_PERMISSION = 'read'
CONST_TOKEN = 'gh...Ic'

CONST_RUNID = datetime.now().strftime("%d%m%Y %H%M%S")

def add_team(repo, team):
    print(f'\n========={repo}={team}===========\nAdding team {team} to repo {repo}')
    url = f'https://api.github.com/orgs/{CONST_ORG}/teams/{CONST_TEAM}/repos/{CONST_ORG}/{repo}'
    print(url)
    payload = {}
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {CONST_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 204:
        log_success(repo)
    else:
        log_error(repo, f'Error adding team to {repo} with code {response.status_code}')

def log_error(repo, message): 
    csv_file = f'{CONST_RUNID}/errors.csv'
    write_csv_file(csv_file, [repo, message])

def log_success(repo): 
    csv_file = f'{CONST_RUNID}/success.csv'
    write_csv_file(csv_file, [repo])

def write_csv_file(csv_file, data):
    print(f'{CONST_RUNID}: {data}')
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    

def read_csv_and_add_team(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            repo = row[0]
            add_team(repo, CONST_TEAM)
            

read_csv_and_add_team('repos.csv')
