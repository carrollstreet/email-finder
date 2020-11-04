#!/usr/bin/env python
# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
import time
import threading

def gitapimails():
    errors = []
    commit_url = []
    mail_list = []
    repolink = []
    owner= []
    gitmail = {}
    try:
        #ввод ника
        nick = input('Enter GitHub User Nickname: ').strip()
        #старт отсчета времени
        start = time.time()
        #поиск по нику в Telegram
        try:
            if len(nick) > 4:
                tlg = requests.get('https://telegram.me/' + nick)
                tlg_soup = BeautifulSoup(tlg.text, 'lxml')
                try:
                    owner.append(tlg_soup.find('div',class_='tgme_page_title').text)
                except AttributeError:
                    pass
                if tlg_soup.find('div', class_="tgme_page_title") == None:
                    print("Can't find such user in Telegram")
                else:
                    if len(owner) > 0:
                        print('Using nickname to find telegram account:')
                        print(f'{owner[0]} - {tlg.url.lower()}')
                    else:
                        print(f'Using nickname to find telegram account: {tlg.url.lower()}')
            else:
                print('Telegram nick must contain more than 4 symbols')
        except:
            print('Wrong nickname for Telegram user')

        #поиск по github api
        url = 'https://api.github.com/users/' + nick + '/events/public'
        req = requests.get(url)
        for i in range(len(req.json())):
            try:
                for j in range(len(req.json())):
                    mail = req.json()[i]['payload']['commits'][j]['author']['email'].lower().strip()
                    name = req.json()[i]['payload']['commits'][j]['author']['name'].lower().strip()
                    gitmail[mail] = name
            except KeyError:
                pass
        
        print()
        if len(gitmail) > 0:
            print('Emails from github public API:')
            for k, i in gitmail.items():
                print('{} - {}'.format(i, k))
        else:
            print('There are no emails in github pubplic API for this profile')
            
        #hireable status
        #url_hr = 'https://api.github.com/users/' + nick 
        #r_hr = requests.get(url_hr)
        #try:
        #    if r_hr.json()['hireable'] == True:
        #        print('Status:  Hireable on GitHub Jobs')
        #    else:
        #        print('Status: NOT Hireable on GitHub Jobs')
        #except:
        #    print("Can't receive hireable status")
        
        #поиск ящиков в коммитах
        print()
        print('Looking for emails in repositories, wait please')
        print()
        try:
            start_url = 'https://github.com/' + nick + '?tab=repositories'
            r = requests.get(start_url)
            soup = BeautifulSoup(r.text, 'lxml')
            name = soup.find('span', class_="p-name vcard-fullname d-block overflow-hidden").text
            
            for i in soup.find_all('div', class_="d-inline-block mb-1"):
                if 'Forked' not in str(i.find('span')) and 'Archived' not in str(i.find('span', class_="Label Label--outline v-align-middle ml-1 mb-1")):
                    repolink.append('https://github.com' + i.find('a').get('href'))
            repolink_master = [str(i) + '/commits/master' for i in repolink]
            
            for z in range(len(repolink_master)):
                try:
                    rep_comm = requests.get(repolink_master[z])
                    soup = BeautifulSoup(rep_comm.text, 'lxml')
                    if (nick.lower() == soup.find('a', class_="commit-author user-mention").text.lower()) or (name == soup.find('span', class_="commit-author user-mention").text) or (name == soup.find('a', class_="commit-author user-mention").text):
                        string = soup.find('a', class_='link-gray-dark text-bold js-navigation-open').get('href')
                        commit = re.findall('/commit/[\w]+', string)[0]
                        commit_url.append(str(repolink[z]) + commit + '.patch')
                    else:
                        continue
                except AttributeError:
                    pass
                
            def worker(url):   
                req_com = requests.get(url)
                try:
                    mails = re.findall('From: ([\w <@.-]+)', req_com.text)[0].replace('<', '- ')
                    mail_list.append(mails.lower().strip())
                except:
                    errors.append(i)
              
            if len(commit_url) < 5:
                for i in commit_url:
                    worker(i)
            else:
                for i in commit_url:
                    t = threading.Thread(target=worker, args=(i,))
                    t.start()
                time.sleep(2)
                    
            if len(mail_list) > 0:
                print('Emails from commit.patch:')
                print('\n'.join(set(mail_list)))
            else:
                print("Can't find any emails in repositories")
        except:
            print("An error has occurred on this step")
        
        if len(errors) > 0:
            print("Can't extrat emails from these commits, you can check it:")
            print('\n'.join(errors))
        timing = 'Emails search took {:.2f} seconds'.format(time.time()-start)
        print(timing)
        for i in range(len(timing)):
            print('-', end='')
        print()
    except:
        print('Something broken')
    print()

def retry():
    return gitapimails(), retry()

retry()