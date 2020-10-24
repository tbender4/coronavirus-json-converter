from git.exc import GitCommandError, NoSuchPathError
from git import Repo
import os
import sys
import datetime
import csv
import json

def find_week_old_commit(skip_to = 0, count=10):
    commits = repo.iter_commits('master', skip=skip_to, max_count=count)
    today = datetime.date.today()
    for commit in commits:
        t = commit.committed_datetime              #datetime commit
        t_date = t.date()
        # t = commit.committed_date               #epoch of commit
        # t_date = datetime.date.fromtimestamp(t)
        delta = today - t_date
#        print(commit, time.asctime(time.gmtime(t)), t, delta.days)
        if delta.days == 7:
            return commit
    else:
        return find_week_old_commit(skip_to=count, count=count)

def gen_list_from_commit(commit='HEAD', zip_codes = []):

    show_arg = '{}:{}'.format(commit, file_name)
    old_data = repo.git.show(show_arg)

    selected_lines = []
    for i in old_data.split('\n'):
        line = i.split('\r')
        line.pop()
        line = line[0].split(',')
        if line[0] in zip_codes:            #saves only wanted zip codes
            selected_lines.append(line)
    return selected_lines

def gen_list_from_local(zip_codes=[]):

    local_copy_csv = os.path.join(repo_name, file_name)
    selected_lines = []
    try:
        with open(local_copy_csv) as csvfile:
            csvreader = csv.reader(csvfile)
            field_names = next(csvreader)    #grabs name of fields
            for line in csvreader:
                if line[0] in zip_codes:
                    selected_lines.append(line)
            return selected_lines
    except IOError as error:
        sys.exit(error)

def get_data_field_names():
    local_copy_csv = os.path.join(repo_name, file_name)
    try:
        with open(local_copy_csv) as csvfile:
            csvreader = csv.reader(csvfile)
            return next(csvreader)
    except IOError as error:
        sys.exit(error)

def gen_dict_from_list(keys=[], data=[]):
    keys = get_data_field_names()       #inner keys
    output = {}                         #outer dict
    for line in data:
        zip_code = line[0]                  #zip code is outer key
        line_dict = dict(zip(keys, line))   #inner value is line converted to dict
        output[zip_code]=line_dict               #adds to outer dict
    
    return output

url = 'https://github.com/nychealth/coronavirus-data'
repo_name = url.split('/')[4]
file_name = 'data-by-modzcta.csv'

try:
    repo = Repo(repo_name)
    repo.remotes.origin.pull()
    #TODO: Pull changes upon each run
except NoSuchPathError:
    try:
        repo = Repo.clone_from(url, repo_name)
    except GitCommandError:
        sys.exit("Failed to clone repo.")
except: #Unknown Error
    sys.exit(sys.exc_info()[0])

# get specific zip codes
zip_codes = []

restaurant_csv = os.path.join('data','restaurants_recoded.csv')
try:
    with open(restaurant_csv) as csvfile:
        csvreader = csv.reader(csvfile)
        field_names = next(csvreader)    #grabs name of fields
#        print(field_names)
        for i in csvreader:
            zip_codes.append(i[1].split(' ')[-1])
except IOError as error:
    sys.exit(error)

old_commit = find_week_old_commit()
old_list = gen_list_from_commit(old_commit, zip_codes)
local_list = gen_list_from_local(zip_codes)

print('week old commit:\n=========')
for i in old_list:
    print(i)

print('\nlocal:\n=========')
for i in local_list:
    print(i)

# print(gen_dict_from_list(data=local_list))
local_dict = gen_dict_from_list(data=local_list)
old_dict = gen_dict_from_list(data=old_list)

latest = os.path.join('data', 'covid_latest.json')
older = os.path.join('data', 'covid_week_old.json')
with open (latest, 'w') as file:
    json.dump(local_dict, file, indent=2)
with open (older, 'w') as file:
    json.dump(old_dict, file, indent=2)

#TODO: Save previous commits to files

#TODO: Report errors by emails/notifs

#TODO: Report mathematical differences. Export to JSON