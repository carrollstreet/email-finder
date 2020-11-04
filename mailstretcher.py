#!/usr/bin/env python
# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
def gitapimails():
    nick = input()
    url = 'https://api.github.com/users/' + nick + '/events/public'
    req = requests.get(url)
    raw = re.findall('"email":"[\w]+@[\w.\w]+"', req.text)
    raw = list(map(lambda x: x.replace('"email":', '').strip('""'), raw))
    mails = ', '.join(set(raw))
    print(f'Emails from github public API: {mails}')
    try:
        start_url = 'https://github.com/' + nick + '?tab=repositories'
        r = requests.get(start_url)
        soup = BeautifulSoup(r.text, 'lxml')
        repolink = []
        for i in soup.find_all('div', class_="d-inline-block mb-1"):
            if 'Forked' not in str(i.find('span')):
                repolink.append('https://github.com' + i.find('a').get('href'))
        repolink_first_commit = str(str(repolink[0]) + '/commits/master')
        rep_comm = requests.get(repolink_first_commit)
        soup = BeautifulSoup(rep_comm.text, 'lxml')
        commit = re.findall('/commit/[\w]+', str(soup.find_all('a')))[0]
        commit_url = str(repolink[0]) + commit + '.patch'
        req_com = requests.get(commit_url)
        mails = re.findall('<[\w@\w.\w]+>',req_com.text)
        print('Email from commit.patch:', ''.join(mails).strip('<>'))
    except:
        pass
def retry():
    return gitapimails(), retry()
retry()
