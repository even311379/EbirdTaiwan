4
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:18:09 2019

@author: DB
"""

import pandas as pd
import datetime
import time
import plotly.graph_objects as go

def draw_bar(values, names):

    if len(values) < 5:
        t = [0]*(5 - len(values))
        values = t.append(values)
        t = ['']*(5 - len(values))
        names = t.append(names)

    data = [
        go.Bar(
            x = values,
            y = [1,2,3,4,5],
            width=[0.5, 0.5, 0.5, 0.5, 0.5],
            marker_color='#5EA232',
            orientation='h',
            hoverinfo = 'text',
            hovertext = [f'{n}: {v}' for n,v in zip(names, values)]
        ),
        go.Scatter(
            x = [max(values)* -0.75] * 5,
            y = [1,2,3,4,5],
            text=[f'<b>{n}</b>' for n in names],
            mode = 'text',
            textposition="middle right",
            textfont=dict(
                color="black",
                size=12,),
            hoverinfo='none'
        ),
         go.Scatter(
            x = [max(values)* 0.05] * 5,
            y = [1,2,3,4,5],
            text=[f'<b>{n}</b>' for n in values],
            mode = 'text',
            textposition="middle right",
            textfont=dict(
                color="white",
                size=18),
            hoverinfo='none'
        )
    ]


    layout = go.Layout(
        shapes = [go.layout.Shape(type="line",x0= max(values)* -0.1,x1=max(values)* -0.1,y0=1,y1=5)],
        margin=dict(
            l=0,r=0,b=0,t=0
        ),
        dragmode = False,
        xaxis=dict(
        range=[max(values)* -0.75, max(values)],
        tickvals = [ 0, int(max(values)/2), max(values)]
        ),
        yaxis=dict(showticklabels=False),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig = go.Figure(data=data, layout=layout)

    return fig



def GetUploadTimeTable(sdate, edate):
    df = pd.read_csv('ActivityTime.csv')
    df = df.fillna('')
    dtl = []
    for d, t in zip(df.Date, df.Time):
        if t == '':
            dts = d + ' 00:00'
        else:
            dts = d + ' ' + t
        
        dtl.append(datetime.datetime.strptime(dts, '%d %b %Y %H:%M'))

    df.insert(0, 'DateTime', pd.Series(dtl))
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs].sort_values(by='DateTime', ascending=False)[['Observer', 'Date', 'Time']]
    if len(ndf) >= 5:
        ndf = ndf.tail(5)
        ndf.insert(0, 'No.', range(1,6))
    else:
        ndf.insert(0, 'No.', range(1,len(ndf)+1))
    ndf.columns = ['名次', '觀察者', '日期', '時間']
    return ndf

def GetN_Participants(sdate, edate):
    df = pd.read_csv('AllData.csv')
    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    return len(set(ndf.Observer.tolist()))


def GetN_Species(sdate, edate):
    df = pd.read_csv('AllData.csv')
    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs].drop_duplicates(['Species','Observer'])
    observers = set(ndf.Observer)
    N_species = []
    for obs in observers:
        N_species.append(len(ndf[ndf.Observer == obs]))
    odf = pd.DataFrame([observers,N_species]).T
    odf.columns = ['觀察者', '鳥種數']
    odf = odf.sort_values(by='鳥種數')
    if len(odf) >= 5:
        odf = odf.tail(5)
        odf.insert(0, '名次', range(1,6))
    else:
        odf.insert(0, '名次', range(1,len(odf)+1))
    
    return odf

'''
problem of 'X' which is transfered to -1 temporarily, ignore it by now
'''
def GetTotalIndivisual(sdate, edate):
    df = pd.read_csv('AllData.csv')
    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    observers = set(ndf.Observer)
    TotalN = []
    for observer in observers:
        N = 0
        for n in ndf[ndf.Observer==observer].Count.tolist():
            if n < 0:
                pass
            else:
                N += n
        TotalN.append(N)
    odf = pd.DataFrame([observers,TotalN]).T
    odf.columns = ['觀察者', '鳥總隻數']
    odf = odf.sort_values(by='鳥總隻數')
    if len(odf) >= 5:
        odf = odf.tail(5)
        odf.insert(0, '名次', range(1,6))
    else:
        odf.insert(0, '名次', range(1,len(odf)+1))
    return odf




def GetN_Record(sdate, edate):
    df = pd.read_csv('AllData.csv')
    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    observers = set(ndf.Observer)
    N_Record = []
    for observer in observers:
        N_Record.append(len(ndf[ndf.Observer==observer]))
    odf = pd.DataFrame([observers,N_Record]).T
    odf.columns = ['觀察者', '紀錄筆數']
    odf = odf.sort_values(by='紀錄筆數')
    if len(odf) >= 5:
        odf = odf.tail(5)
        odf.insert(0, '名次', range(1,6))
    else:
        odf.insert(0, '名次', range(1,len(odf)+1))
    
    return odf


if __name__ == "__main__":        
    pass