# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import re
import pandas as pd
import time
import datetime

options = Options()
options.add_argument('--headless')

IDs = ['ET黑面琵鷺隊', 'ET灰面鵟鷹隊','ET小辮鴴隊']
PWs = ['201910BFS','201910GFB','201910NL']
DFs = ['Team1Data.csv', 'Team2Data.csv', 'Team3Data.csv']


def my_logger(level, message):
    
    if level == 0:
        L = '***INFO**'
    elif level == 1:
        L = '*WARNING*'
    elif level == 2:
        L = '**ERROR**'
    
    with open('UpdateAutumnData.log', 'a+', encoding='utf-8') as f:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{L} {t}: {message}  \n')


def GetChecklist(url, c):
    r = requests.get(url)
    time.sleep(1)
    S = re.findall('Heading-main\".*?>(.*?)</span',r.text)[4:]
    '''
    if the check list is hidden from public, this word "Checklist flagged"
    will occur in its html source code and crash my program, I'lljust explicitly silence it!
    '''
    if 'Checklist flagged' in S:  
        S.remove('Checklist flagged')
    N = [-1 if n == 'X' else int(n) for n in re.findall('<span>([X|\d]\d*?)</span>',r.text)]
    t = re.findall('<span class="Heading-sub Heading-sub--inline">(.*?)</span>', r.text)[0]
    d = re.findall('</span>(.*?)</span>',r.text)[0]
    DT = t+d
    try:
        L = re.findall('href="(.*?/hotspot/.*?)"', r.text)[0]
    except:
        L = re.findall('Location</h6>\s*?<span>([\S\s]*?)</span>', r.text)[0]
        if '\n' in L:
            L = L[L.index('\n')+1:]
        
    return pd.DataFrame(dict(Creator=[c]*len(S),Species=S,Count=N,DateTime=[DT]*len(S),Hotspot=[L]*len(S),url=[url]*len(S)))


def Update(j = 0):
    driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', options = options)
    time.sleep(3)
    try:
        driver.get('https://secure.birds.cornell.edu/cassso/login?')
        time.sleep(5)
        ele_n = driver.find_element_by_name('username')
        ele_p = driver.find_element_by_name('password')
        ele_submit = driver.find_element_by_id('form-submit')
        ele_n.send_keys(IDs[j])
        time.sleep(1)
        ele_p.send_keys(PWs[j])
        time.sleep(1)
        ele_submit.click()
            
        driver.get('https://ebird.org/shared')
        time.sleep(5)
        btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == 'Accept' or b.text == 'Keep']
        time.sleep(3)

        N = len(btns) * 10 + 1
        while btns:
            btns[0].click()
            time.sleep(5)
            btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == 'Accept' or b.text == 'Keep']
            N -= 1
            if N <= 0:
                my_logger(2, f'infinite loop for clicking btns for {IDs[j]}')
                return False

        cs = [i.text for i in driver.find_elements_by_class_name('dataCell') if i.get_attribute('headers') == 'owner']
        cls = [i.get_attribute('href') for i in driver.find_elements_by_link_text('View or Edit')]

    except Exception as e:
        my_logger(2, f'selenium fail for {IDs[j]}: {e}')
        driver.close()
        return False

    driver.close()
    
    WTS = [] # what to scrap
    Creators = []
    if not os.path.isfile('data/'+DFs[j]):
        WTS = cls
        Creators = cs
    else:
        old_url = pd.read_csv('data/'+DFs[j]).url.drop_duplicates().tolist()
        WTS = [url for url in cls if url not in old_url]
        Creators = [cs[i] for i, url in enumerate(cls) if url not in old_url]
    if len(WTS) == 0:
        my_logger(1, f'No new shared data for {IDs[j]}!')
        return False
    
    DLS = []   
    for i, c in zip(WTS, Creators):
        try:
            DLS.append(GetChecklist(i, c))
        except Exception as e:
            my_logger(2, f'Scrape Data failed for : {e}')

    if len(DLS) == 0:
        my_logger(2, f'Fail to scrape any data for {IDs[j]}!')
        return False   
    
    DATA = pd.concat(DLS).reset_index(drop=True)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    DATA.insert(0, 'ScrapDate', [today]*len(DATA))

    if not os.path.isfile(DFs[j]):
        DATA.to_csv(DFs[j],index=False)
    else:
        old_data = pd.read_csv(DFs[j])
        more_data = old_data.append(DATA, ignore_index=True)
        more_data.to_csv('data/'+DFs[j],index=False)
    
    my_logger(0, f'Success Scrape {IDs[j]}')

# download Data At AM 03:00        
def automate():
    while True:
        now = time.localtime()
        sleeptime = ((26 - now.tm_hour) * 60 + (60 - now.tm_min))*60
        time.sleep(sleeptime)
        for i in range(3):
            Update(i)
 
if __name__ == '__main__':
    automate()
