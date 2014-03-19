#!/usr/bin/python

import ConfigParser
import os.path
from redmine import Redmine
import requests
import string
import sys


def get_config_value(section, option):
    cp = ConfigParser.ConfigParser()
    cp.read('config.ini')
    try:
        return cp.get(section, option)
    except:
        return None


def main():
    #check config file is present or not
    if not os.path.isfile('config.ini'):
        print "ERROR :: config file is missing"
        sys.exit(1)

    #read the config file and populate the data
    github = {'git_username': '', 'git_password': '', 'repos': ''}
    for key in github.iterkeys():
        github[key] = get_config_value('GITHUB', key)

    redmine = {'rm_username': '', 'rm_password': '', 'id': '',
               'apikey': '', 'url': ''}
    for key in redmine.iterkeys():
        redmine[key] = get_config_value('REDMINE', key)

    if redmine['apikey'] is not None or redmine['apikey'] != '':
        r = Redmine(redmine['url'], key = redmine['apikey'])
    else:
        r = Redmine(redmine['url'], username = redmine['rm_username'],
                    password = redmine['rm_password'])
    issue_count = 0
    for repo in string.split(github['repos']):
        url = 'https://api.github.com/repos/%s/issues' % repo
        response = requests.get(url)
        if response.status_code != 200:
            print "WARNING :: can't get issue for repo: %s\
                   \n%s : Error code:%s" % (repo, repo, response.status_code)
            continue
        for issue in response.json():
            if issue['state'] != 'open':
                continue
            subject = issue['title']
            description = issue['body']
            try:
                issue = r.issue.create(project_id = redmine['id'],
                                       subject = subject,
                                       tracker_id = 1,
                                       status_id = 1,
                                       priority_id = 4,
                                       description = description)
            except:
                continue
            issue_count = issue_count + 1

    print '{0} issues are created in project id {1}'.format(issue_count,
                                                         redmine['id'])

if __name__ == '__main__':
    main()
