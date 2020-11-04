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
    print('Looking for emails in repositories, It may take up to 60 sec, wait please')   
    try:
        start_url = 'https://github.com/' + nick + '?tab=repositories'
        r = requests.get(start_url)
        soup = BeautifulSoup(r.text, 'lxml')
        repolink = []
        for i in soup.find_all('div', class_="d-inline-block mb-1"):
            if 'Forked' not in str(i.find('span')) and 'Archived' not in str(i.find('span', class_="Label Label--outline v-align-middle ml-1 mb-1")):
                repolink.append('https://github.com' + i.find('a').get('href'))
        repolink_master = [str(i) + '/commits/master' for i in repolink]
        commit_url = []
        for z in range(len(repolink_master)):
            try:
                rep_comm = requests.get(repolink_master[z])
                soup = BeautifulSoup(rep_comm.text, 'lxml')
                for i in soup.find_all('li', class_='commit Box-row Box-row--focus-gray mt-0 p-2 d-flex js-commits-list-item js-navigation-item js-details-container Details js-socket-channel js-updatable-content'):
                    if nick.lower() == i.find('a', class_="commit-author tooltipped tooltipped-s user-mention").text.lower():
                        string = i.find('a').get('href')
                        commit = re.findall('/commit/[\w]+', string)[0]
                        commit_url.append(str(repolink[z]) + commit + '.patch')
                        break
            except:
                pass
            mail_list = []
            for i in commit_url:
                try:
                    req_com = requests.get(i)
                    mails = re.findall('<[\w.]+@[\w.]+>',req_com.text)[0]
                    mail_list.append(''.join(mails).strip('<>'))
                except:
                    pass
        if len(mail_list) > 0:
            print('Emails from commit.patch:', ', '.join(set(mail_list)))
        else:
            print("Can't find any emails in repositories") 
    except:
        print("Can't find any emails in repositories")
        pass
    print('Emails search took {:.2f} seconds'.format(time.time()-start))
    print()
    
def retry():
    return gitapimails(), retry()

retry()
