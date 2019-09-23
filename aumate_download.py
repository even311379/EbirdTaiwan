import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import datetime
import re


def my_logger(level, message):
    
    if level == 0:
        L = '***INFO**'
    elif level == 1:
        L = '*WARNING*'
    elif level == 2:
        L = '**ERROR**'
    
    with open('UpdateData.log', 'a+') as f:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{L} {t}: {message}  \n')
        

location_id = ['L2425949', 'L3856620', 'L5248567', 'L5569845', 'L5192267', 'L3290632',
              'L5594364', 'L5569795', 'L6675201', 'L8443148', 'L5569882', 'L7033433',
             'L3949628', 'L2894596', 'L2329696', 'L3887194', 'L2394672',
            'L3188784', 'L6563827', 'L2270945']


def download_all():
    global failed_loc
    global failed_checklist

    DFL = []
    for loc in location_id:
        try:
            r = requests.get('https://ebird.org/hotspot/'+loc+'/activity?yr=all&m=')
            time.sleep(2)
            soup = BeautifulSoup(r.text, 'html.parser')
            date_str_list = [i.contents[1].contents[0].replace('\t','').replace('\n','')[:-1] for i in soup.find_all("td",class_="obstable-date")]
            date_list = [time.strptime(s, '%d %b %Y') for s in date_str_list]
            checklist_urls = [i.contents[1]['href'] for i in soup.find_all("td",class_="obstable-date")]
            observer_list = [i.contents[0] for i in soup.find_all("td",class_="species-name recent-visitor")]
            temp_d = []
            temp_c = []
            temp_o = []
            for i, d in enumerate(date_list):
                if d.tm_year == 2019 and d.tm_mon >= 6:
                    temp_d.append(d)
                    temp_c.append(checklist_urls[i])
                    temp_o.append(observer_list[i])
            if len(temp_c) > 0:
                print(f'Obs after 2019/6/01 is found!! {loc}')
            else:
                print(f'There is no obs after 2019/6/01: {loc}')
                continue
                
            
            dl = []
            for i, url in enumerate(temp_c):
                try:
                    r = requests.get('https://ebird.org'+url)
                    time.sleep(1)
                    S = re.findall('Heading-main\".*?>(.*?)</span',r.text)[4:]
                    N = [-1 if n == 'X' else int(n) for n in re.findall('<span>(..?.?)</span>',r.text)]
                    temp_df = pd.DataFrame(dict(Date = [temp_d[i]]*len(S),Observer = [temp_o[i]]*len(S),Species=S,Count=N, Link=[url]*len(S)))
                    dl.append(temp_df)
                except Exception as e:
                    print(e)
                    print(url)
                    failed_checklist.append(loc+':'+url)

            LocDF = pd.concat(dl).reset_index(drop=True)
            LocDF.insert(0, 'LocationID', [loc]*len(LocDF))
            DFL.append(LocDF)
            print(len(DFL))

        except Exception as e:
            print(loc)
            print(e)
            failed_loc.append(loc)


    DF = pd.concat(DFL).reset_index(drop=True)
    DF['Date'] = DF['Date'].apply(lambda x: f'{x.tm_year}-{x.tm_mon}-{x.tm_mday}')
    DF.to_csv('AllData.csv',index=False)
    return DF


def update_data():

    my_logger(0, 'Start update data.')
    old_data = pd.read_csv('AllData.csv')
    old_Link = old_data.Link.tolist()
    th_day = datetime.datetime.now() - datetime.timedelta(days=30)

    DFL = []
    for loc in location_id:
        try:
            r = requests.get('https://ebird.org/hotspot/'+loc+'/activity?yr=all&m=')
            time.sleep(2)
            soup = BeautifulSoup(r.text, 'html.parser')
            date_str_list = [i.contents[1].contents[0].replace('\t','').replace('\n','')[:-1] for i in soup.find_all("td",class_="obstable-date")]
            date_list = [datetime.datetime.strptime(s, '%d %b %Y') for s in date_str_list]
            checklist_urls = [i.contents[1]['href'] for i in soup.find_all("td",class_="obstable-date")]
            observer_list = [i.contents[0] for i in soup.find_all("td",class_="species-name recent-visitor")]
            temp_d = []
            temp_c = []
            temp_o = []
            for i, d in enumerate(date_list):
                if d > th_day:
                    if checklist_urls[i] not in old_Link :
                        temp_d.append(d.strftime("%Y-%m-%d"))
                        temp_c.append(checklist_urls[i])
                        temp_o.append(observer_list[i])
        
            r = requests.get('https://ebird.org/hotspot/'+ loc +'?yr=all&m=&rank=mrec')
            time.sleep(2)
            hrefs = re.findall('href=\"(/view.*?)\">\d',r.text)
            odate = re.findall('href=\"/view.*?\">(.*?)</a>',r.text)
            wdf = pd.read_html(r.text)
            if len(wdf) > 1:
                Bys = wdf[2]['By'].dropna().tolist()
            else:
                Bys = wdf[0]['By'].dropna().tolist()
            hrefs = list(dict.fromkeys(hrefs))[:10]
            odate = list(dict.fromkeys(odate))[:10]
            Bys = list(dict.fromkeys(Bys))[:10]

            for h,o,b in zip(hrefs,odate,Bys):
                d = datetime.datetime.strptime(o,'%d %b %Y')
                if d > th_day:
                    if h not in old_Link + temp_c:
                        temp_d.append(d.strftime("%Y-%m-%d"))
                        temp_c.append(h)
                        temp_o.append(b)
            if len(temp_c) > 0:
                print(f'New data found in {loc}!!!!!')
            else:
                continue
            
            dl = []
            for i, url in enumerate(temp_c):
                try:
                    r = requests.get('https://ebird.org'+url)
                    time.sleep(1)
                    S = re.findall('Heading-main\".*?>(.*?)</span',r.text)[4:]
                    N = [-1 if n == 'X' else int(n) for n in re.findall('<span>(..?.?)</span>',r.text)]
                    temp_df = pd.DataFrame(dict(Date = [temp_d[i]]*len(S),Observer = [temp_o[i]]*len(S),Species=S,Count=N, Link=[url]*len(S)))
                    dl.append(temp_df)
                except Exception as e:
                    my_logger(2, f'Fail to scape this checklist: {url} due to {e} ')
                    print(url)

            LocDF = pd.concat(dl).reset_index(drop=True)
            LocDF.insert(0, 'LocationID', [loc]*len(LocDF))
            DFL.append(LocDF)
        
        except Exception as e:
            my_logger(2, f'Fail to scape this location: {loc} due to {e} ')
            
    
    if DFL:
        DF = pd.concat(DFL).reset_index(drop=True)
        more_data = old_data.append(DF, ignore_index=True)
        more_data.to_csv('AllData.csv',index=False)        
        my_logger(1, f'New data found: {len(more_data) - len(old_data)} rows')
    else:
        my_logger(1, 'No new data found!')
    
    my_logger(0, 'Data updating process is finished!')
        


def automate():
    start = False
    while True:
        if not start:
            time.sleep(60)
            if time.localtime().tm_min == 0:
                start = True
        else:
            time.sleep((60 - time.localtime().tm_min) + 2 * 60)
            update_data()


if __name__ == '__main__':
    automate()
    