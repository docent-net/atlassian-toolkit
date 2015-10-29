#!/usr/bin/python

import pygit2
import os
import requests
from requests.auth import HTTPBasicAuth

username = 'username'
password = 'password'
cred = pygit2.UserPass(username, password)

ommit_repos = ('some_repo')

STASH_API_URL = 'http://stash_url/rest/api/1.0'
PROJECTS_JSON_URL = "%s/%s" % (STASH_API_URL, 'projects?name&permission&limit=1000')

ARCHIVE_DIR = '/directory/where/you/want/to/clone/repos'

req = requests.get(PROJECTS_JSON_URL, auth=HTTPBasicAuth(username, password))

for _project in req.json()['values']:
    REPOS_JSON_URL = "%s/projects/%s/repos" % (STASH_API_URL, _project['key'])

    if not os.path.exists("%s/%s" % (ARCHIVE_DIR, _project['key'])):
        os.mkdir("%s/%s" % (ARCHIVE_DIR, _project['key']))

    req_repos = requests.get(REPOS_JSON_URL, auth=HTTPBasicAuth(username, password))
    for _repo in req_repos.json()['values']:
        print _repo['cloneUrl']

        if _repo['name'] in ommit_repos:
            print "ommiting %s" % _repo['name']
            continue;

        if not os.path.exists("%s/%s/%s" % (ARCHIVE_DIR, _project['key'], _repo['name'])):
            pygit2.clone_repository(_repo['cloneUrl'], "%s/%s/%s" % (ARCHIVE_DIR, _project['key'], _repo['name']), bare=False, credentials=cred)