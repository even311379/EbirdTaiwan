4
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:18:09 2019

@author: DB
"""

import pandas as pd
import datetime
import time
import random
import plotly.graph_objects as go

## app1 functions
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
        tickvals = [ 0, int(max(values)/2), max(values)],
        showgrid=False,zeroline=False
        ),
        yaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
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

# app2 functions
def half_donut(n_bird, n_rows, team = 0, w = 1600):
    
    if team == 0:
        team_name = '灰面鵟鷹隊'
        team_color = '#A4B924'
    elif team == 1:
        team_name = '黑面琵鷺隊'
        team_color = '#5185AA'
    elif team == 2:
        team_name = '小辮鴴隊'
        team_color = '#993131'

    if 681 <= w:
        fig_wh = 350
        t1_s = 24
        t2_s = 30
        t3_s = 48
    elif 400 <= w < 681:
        fig_wh = 350
        t1_s = 20
        t2_s = 24
        t3_s = 32
    else:
        fig_wh = 300
        t1_s = 16
        t2_s = 20
        t3_s = 28

    all_n_bird = 654
    values = [n_bird, all_n_bird - n_bird ,all_n_bird]
    if n_bird > all_n_bird / 2:
        D = 'clockwise'
    else:
        D = 'counterclockwise'

    data=[go.Pie(values=values,
                 marker=dict(colors=[team_color,'#C4C4C4','rgba(0,0,0,0)']),hole=.75,
                 rotation =90,direction=D,
                 text=[f'發現了{n_bird}種囉!', f'還有{all_n_bird - n_bird}種等待您的發掘',''],
                 textinfo='none',
                 hoverinfo='text'
                )]

    layout = go.Layout(
        width=fig_wh,
        height=fig_wh,
        clickmode='none',
        dragmode=False,
        margin=dict(l=0,r=0,b=0,t=0),
        xaxis=dict(range=[-10,10],showticklabels=False,showgrid=False,zeroline=False,automargin=True),
        yaxis=dict(range=[-10,10],showticklabels=False,showgrid=False,zeroline=False,automargin=True),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[
            go.layout.Annotation(x=0,y=3,xref="x",yref="y",text=f"鳥種數：{n_bird}",font=dict(size=t1_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=0,y=-2,xref="x",yref="y",text=f"總上傳清單數：{n_rows}",font=dict(size=t2_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=0,y=-5,xref="x",yref="y",text=team_name,font=dict(size=t3_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            #go.layout.Annotation(x=0,y=-7,xref="x",yref="y",text="1345",font=dict(size=10,color='rgba(0,0,0,0)'),showarrow=False),#to prevent chinese text been cut off
        ]
    )
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=data,layout=layout)
    return fig


def accumlate_people_trace(start_date):
    
    data1 = pd.read_csv('Team1Data.csv')
    data2 = pd.read_csv('Team2Data.csv')
    data3 = pd.read_csv('Team3Data.csv')

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    def GetXY(data):
        DaysAfterStart = [(datetime.datetime.strptime(ds, '%Y-%m-%d') - start_date).days for ds in data.ScrapDate]
        data.insert(0, 'DAS', DaysAfterStart)
        X = []
        Y = []
        for i in set(DaysAfterStart):
            X.append(i+1)
            Y.append(len(set(data[data.DAS <= i].Creator.tolist())))
        return X ,Y
    
    x1, y1 = GetXY(data1)
    x2, y2 = GetXY(data2)
    x3, y3 = GetXY(data3)

    y_upper = max(y1+y2+y3)*1.2 # hack y axis limit

    data = [        
        go.Scatter(x = x1, y = y1, mode='lines+markers',line=dict(shape='spline',color='#A4B924'), name = '灰面鵟鷹隊'),
        go.Scatter(x = x2, y = y2, mode='lines+markers',line=dict(shape='spline',color='#5185AA'), name = '黑面琵鷺隊'),
        go.Scatter(x = x3, y = y3, mode='lines+markers',line=dict(shape='spline',color='#993131'), name = '小辮鴴隊'),
    ]

    date_text = [f'10/{i}' for i in range(1,32)]

    # brutal force to axis...
    layout = go.Layout(
        shapes = [go.layout.Shape(type="line",x0=0,x1=31,y0=0,y1=0,line=dict(color="#000000",width=1)),
                  go.layout.Shape(type="line",x0=0,x1=0,y0=0,y1=y_upper,line=dict(color="#000000",width=1)),
                 ],
        width=1200,
        height=400,
        margin=dict(l=0,r=0,b=100,t=0),
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True,ticktext=date_text,tickvals=list(range(31))),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True),
        showlegend=False,
        autosize=True,
        hovermode="x",
        clickmode='none',
        dragmode=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[
            go.layout.Annotation(x=30,y= -0.1,xref="x",yref="paper",text="<b>時間</b>",font=dict(size=24,color='#000000',family='Noto Sans TC'),showarrow=False),
            #go.layout.Annotation(x=30,y=-0.4,xref="x",yref="paper",text="1111",font=dict(size=24,color='rgba(0,0,0,0)'),showarrow=False),
            go.layout.Annotation(x=-1.2,y=0.8,xref="x",yref="paper",text="<b>各隊累積人數</b>",font=dict(size=24,color='#000000',family='Noto Sans TC'),showarrow=False,textangle=-90),
            go.layout.Annotation(x=31,y=0,ax=-10,ay=0,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),
            go.layout.Annotation(x=0,y=y_upper,ax=0,ay=15,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),
        ]
    )

    fig = go.Figure(data=data,layout=layout)
    return fig

if __name__ == "__main__":        
    pass