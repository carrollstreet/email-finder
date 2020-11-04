#!/usr/bin/env python
# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
import time

def gitapimails():
    nick = input()
    start = time.time()
    url = 'https://api.github.com/users/' + nick + '/events/public'
    req = requests.get(url)
    raw = re.findall('"email":"[\w.]+@[\w.]+"', req.text)
    raw = list(map(lambda x: x.replace('"email":', '').strip('""'), raw))
    mails = set(raw)
    print()
    if len(mails) > 0:
        print('Emails from github public API:', ', '.join(mails))
    else:
        print('There are no emails in github pubplic API for this profile')
    print('Looking for emails in repositories, wait please')
    try:
        start_url = 'https://github.com/' + nick + '?tab=repositories'
        r = requests.get(start_url)
        soup = BeautifulSoup(r.text, 'lxml')
        repolink = []
        for i in soup.find_all('div', class_="d-inline-block mb-1"):
            if 'Forked' not in str(i.find('span')):
                repolink.append('https://github.com' + i.find('a').get('href'))
        repolink_first_commit = [str(i) + '/commits/master' for i in repolink]
        mail_list = []
        for k, i in enumerate(repolink_first_commit):
            try:
                rep_comm = requests.get(i)
                soup = BeautifulSoup(rep_comm.text, 'lxml')
                commit = re.findall('/commit/[\w]+', str(soup.find_all('a')))[0]
                commit_url = str(repolink[k]) + commit + '.patch'
                req_com = requests.get(commit_url)
                mails = re.findall('<[\w.]+@[\w.]+>',req_com.text)[0]
                mail_list.append(''.join(mails).strip('<>'))
            except:
                pass
        if len(mail_list) > 0:
            print('Emails from commit.patch:', ', '.join(set(mail_list)))
        else:
            print("Can't find any emails in repositories")
    except:
        print('Error')
        pass
    print('Emails search took {:.2f} seconds'.format(time.time()- start))
    print()

def retry():
    return gitapimails(), retry()

retry()
