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
    
def retry():
    return gitapimails(), retry()
retry()

