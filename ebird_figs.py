# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import time
import random
import plotly.graph_objects as go
import dash_table
## app1 functions
def draw_bar(values, names, w):

    # for case that the total df is empty, when the chanllenge just begun, and no data can be scraped yet!
    empty_plot = False
    try:
        if len(values) < 5:
            t = [0] * (5 - len(values))
            values = t + values
            t = [' '] * (5 - len(names))
            names = t + names
    except:
        empty_plot = True
        values= [0] * 5
        names = [''] * 5

    m_names = []
    if w < 400:
        for n in names:
            c_ord = sum([ord(c) for c in n])
            if (c_ord > 40000 and len(n)> 6) or (len(n) > 15):
                if c_ord > 40000:
                    m_names.append(n[:6]+'...')
                else:
                    m_names.append(n[:12]+'...')
            else:
                m_names.append(n)
    else:
        for n in names:
            c_ord = sum([ord(c) for c in n])
            if (c_ord > 60000 and len(n)> 12) or (len(n) > 30):
                if c_ord > 40000:
                    m_names.append(n[:12]+'...')
                else:
                    m_names.append(n[:30]+'...')
            else:
                m_names.append(n)


    data = [go.Bar(x = values,
            y = [1,2,3,4,5],
            width=[0.5, 0.5, 0.5, 0.5, 0.5],
            marker_color='#5EA232',
            orientation='h',
            hoverinfo = 'text',
            hovertext = [f'{n}: {v}' for n,v in zip(names, values)]),
        go.Scatter(x = [max(values) * -0.75] * 5,
            y = [1,2,3,4,5],
            text=[f'<b>{n}</b>' for n in m_names],  # this line to fix final issue...
            mode = 'text',
            textposition="middle right",
            textfont=dict(color="black",
                family='Noto Sans TC',
                size=12,),
            hoverinfo='none'),
        ]

    # set color issue
    anno_text = [f'<b>{n}</b>' if n > 0 else ' ' for n in values]
    if not empty_plot:
        data += [go.Scatter(x = [max(values) * 0.05] * 5,
                y = [1,2,3,4,5],
                text=anno_text,
                mode = 'text',
                textposition="middle right",
                textfont=dict(
                    color='white',
                    family='Noto Sans TC',
                    size=17),
                hoverinfo='none')]

    if empty_plot:
        layout = go.Layout(
            annotations=[go.layout.Annotation(x=0.5, y=3,xref="x",yref="y",
                text="NO DATA YET!",showarrow=False,
                font=dict(family='Noto Sans TC',size=32)
            )],
            margin=dict(l=0,r=0,b=0,t=0),
            dragmode = False,
            xaxis=dict(range=[0,1],showticklabels=False,showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            showlegend=False,
            font=dict(family='Noto Sans TC'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',)
    else:
        layout = go.Layout(shapes = [go.layout.Shape(type="line",x0= max(values) * -0.1,x1=max(values) * -0.1,y0=1,y1=5)],
            margin=dict(l=0,r=0,b=0,t=0),
            dragmode = False,
            xaxis=dict(range=[max(values) * -0.75, max(values)],
            tickvals = [0, int(max(values) / 2), max(values)],
            showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            showlegend=False,
            font=dict(family='Noto Sans TC'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',)

    fig = go.Figure(data=data, layout=layout)

    return fig

def GetUploadTimeTable(sdate, edate):
    df = pd.read_csv('data/ActivityTime.csv')
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
        ndf.insert(0, 'No.', range(1,len(ndf) + 1))
    ndf.columns = ['名次', '觀察者', '日期', '時間']
    return ndf

def GetN_Participants(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

    # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']

    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    return len(set(ndf.Observer.tolist()))

def Get_All_N_Species(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

    # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']

    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    return len(set(ndf.Species.tolist()))

def Get_All_N_List(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

    # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']

    dtl = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.Date]
    bs = []
    for i in dtl:
        if datetime.datetime(sdate[0], sdate[1], sdate[2]) <= i <= datetime.datetime(edate[0], edate[1], edate[2]):
            bs.append(True)
        else:
            bs.append(False)
    ndf = df[bs]
    
    return len(set(ndf.Link.tolist()))

def GetN_Species(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

        # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']

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
        odf.insert(0, '名次', range(1,len(odf) + 1))
    
    return odf

def GetTotalIndivisual(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

        # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']


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
        for n in ndf[ndf.Observer == observer].Count.tolist():
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
        odf.insert(0, '名次', range(1,len(odf) + 1))
    return odf

def GetN_Record(sdate, edate):
    df = pd.read_csv('data/AllData.csv')

        # remove the three teams in case ...
    df = df[df.Observer != '黑面琵鷺隊 eBirdTaiwan']
    df = df[df.Observer != '灰面鵟鷹隊 eBirdTaiwan']
    df = df[df.Observer != '小辮鴴隊 eBirdTaiwan']

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
    ndf = ndf.drop_duplicates(['Observer','Link'])
    for observer in observers:
        N_Record.append(len(ndf[ndf.Observer == observer]))
    odf = pd.DataFrame([observers,N_Record]).T
    odf.columns = ['觀察者', '紀錄筆數']
    odf = odf.sort_values(by='紀錄筆數')
    if len(odf) >= 5:
        odf = odf.tail(5)
        odf.insert(0, '名次', range(1,6))
    else:
        odf.insert(0, '名次', range(1,len(odf) + 1))
    
    return odf

# app2 functions
def half_donut(n_bird, n_rows, team=0, w=1600):
    
    if team == 0:
        team_name = 'ET灰面鵟鷹隊'
        team_color = '#A4B924'
    elif team == 1:
        team_name = 'ET黑面琵鷺隊'
        team_color = '#5185AA'
    elif team == 2:
        team_name = 'ET小辮鴴隊'
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

    if n_bird > 0:
        rot = 90
    else:
        rot = -90
    data = [go.Pie(values=values,
                 marker=dict(colors=[team_color,'#C4C4C4','rgba(0,0,0,0)']),hole=.75,
                 rotation =rot,direction=D,
                 text=[f'發現了{n_bird}種囉!', f'還有{all_n_bird - n_bird}種等待您的發掘',''],
                 textinfo='none',
                 hoverinfo='text')]

    layout = go.Layout(width=fig_wh,
        height=fig_wh,
        clickmode='none',
        dragmode=False,
        margin=dict(l=0,r=0,b=0,t=0),
        xaxis=dict(range=[-10,10],showticklabels=False,showgrid=False,zeroline=False,automargin=True),
        yaxis=dict(range=[-10,10],showticklabels=False,showgrid=False,zeroline=False,automargin=True),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[go.layout.Annotation(x=0,y=3,xref="x",yref="y",text=f"鳥種數：{n_bird}",font=dict(size=t1_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=0,y=-2,xref="x",yref="y",text=f"總上傳清單數：{n_rows}",font=dict(size=t2_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=0,y=-5,xref="x",yref="y",text=team_name,font=dict(size=t3_s,color='#000000',family='Noto Sans TC'),showarrow=False),
            #go.layout.Annotation(x=0,y=-7,xref="x",yref="y",text="1345",font=dict(size=10,color='rgba(0,0,0,0)'),showarrow=False),#to
            #prevent chinese text been cut off
        ])
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=data,layout=layout)
    return fig

def setup_donuts(w, start_date):
    data1 = pd.read_csv('data/Team1Data.csv')
    data2 = pd.read_csv('data/Team2Data.csv')
    data3 = pd.read_csv('data/Team3Data.csv')

    db1 = []
    db2 = []
    db3 = []
    for d in data1.DateTime:
        db1.append(datetime.datetime.strptime(d, '%I:%M %p %d %b %Y') >= start_date)
    for d in data2.DateTime:
        db2.append(datetime.datetime.strptime(d, '%I:%M %p %d %b %Y') >= start_date)
    for d in data3.DateTime:
        db3.append(datetime.datetime.strptime(d, '%I:%M %p %d %b %Y') >= start_date)
            
    
    data1 = data1[db1]
    data2 = data2[db2]
    data3 = data3[db3]

    ts1 = len(set(data1.Species.tolist()))
    tl1 = len(data1[['DateTime', 'Creator']].drop_duplicates())
    ts2 = len(set(data2.Species.tolist()))
    tl2 = len(data2[['DateTime', 'Creator']].drop_duplicates())
    ts3 = len(set(data3.Species.tolist()))
    tl3 = len(data3[['DateTime', 'Creator']].drop_duplicates())

    fig1 = half_donut(ts1,tl1,0,w)
    fig2 = half_donut(ts2,tl2,1,w)
    fig3 = half_donut(ts3,tl3,2,w)
    return fig1, fig2, fig3


def accumlate_people_trace(start_date, w):
    
    if w > 1200:
        ww = 750
        h = 350
        lbs = 24
        tp = -0.15
        ap = -1.2
    elif w > 600:
        ww = 600
        h = 300
        lbs = 22
        tp = -0.15
        ap = -1.2
    else:
        ww = 340
        h = 170
        lbs = 16
        tp = -0.3
        ap = -1.5

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    #today = datetime.datetime(2019,10,1)
    today = datetime.datetime.now()    

    SignUp = pd.read_csv('data/SignUp.csv')
    def GetXYfromSignUp(team = 'ET灰面鵟鷹隊'):
        temp_data = SignUp[SignUp.Team == team]
        DaysAfterStart = [(datetime.datetime.strptime(ds, '%Y-%m-%d') - start_date).days for ds in temp_data.SignUpDate]
        temp_data.insert(0, 'DAS', DaysAfterStart)
        X = []
        Y = []
        DAS_L = list(set(DaysAfterStart))
        DAS_L.sort()
        for i in DAS_L:
            X.append(i+1)
            Y.append(len(temp_data[temp_data.DAS <= i]))
        X = [0] + X
        Y = [0] + Y

        dd = (today - start_date).days + 1
        if dd not in X:
            X.append(dd)
            Y.append(max(Y))

        Date = [(start_date + datetime.timedelta(days=(x-1))).strftime('%m/%d') for x in X]
        return X,Y, Date

    x1, y1, Date1 = GetXYfromSignUp('ET灰面鵟鷹隊')
    x2, y2, Date2 = GetXYfromSignUp('ET黑面琵鷺隊')
    x3, y3, Date3 = GetXYfromSignUp('ET小辮鴴隊')

    t1_info =[''] + [f'{d}: 灰面鵟鷹隊有{t}位成員囉' for t, d in zip(y1[1:],Date1[1:])]
    t2_info =[''] + [f'{d}: 黑面琵鷺隊有{t}位成員囉' for t, d in zip(y2[1:],Date2[1:])]
    t3_info =[''] + [f'{d}: 小辮鴴隊有{t}位成員囉' for t, d in zip(y3[1:],Date3[1:])]

    y_upper = max(y1 + y2 + y3) * 1.2 # hack y axis limit

    data = [go.Scatter(x = x1, y = y1, mode='lines',line=dict(shape='spline',color='#A4B924'), name = 'ET灰面鵟鷹隊', hoverinfo = 'text', text=t1_info),
        go.Scatter(x = x2, y = y2, mode='lines',line=dict(shape='spline',color='#5185AA'), name = 'ET黑面琵鷺隊', hoverinfo = 'text', text=t2_info),
        go.Scatter(x = x3, y = y3, mode='lines',line=dict(shape='spline',color='#993131'), name = 'ET小辮鴴隊', hoverinfo = 'text', text=t3_info),]

    date_text = [''] + [f'10/{i+1}' for i in range(31)]

    # brutal force to axis...
    layout = go.Layout(shapes = [go.layout.Shape(type="line",x0=0,x1=21,y0=0,y1=0,line=dict(color="#000000",width=1)),
                  go.layout.Shape(type="line",x0=0,x1=0,y0=0,y1=y_upper,line=dict(color="#000000",width=1)),],
        width=ww,
        height=h,
        margin=dict(l=0,r=0,b=50,t=0),
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True,ticktext=date_text,tickvals=list(range(20))),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True,fixedrange=True,range=[0, y_upper*1.2]),
        showlegend=True,
        legend=dict(x=0.8, y=0.1),
        autosize=True,
        hovermode="x",
        #clickmode='none',
        dragmode='pan',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[go.layout.Annotation(x=20,y= tp,xref="x",yref="paper",text="時間",font=dict(size=lbs,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=ap,y=0.8,xref="x",yref="paper",text="各隊累積人數",font=dict(size=lbs,color='#000000',family='Noto Sans TC'),showarrow=False,textangle=-90),
            go.layout.Annotation(x=21,y=0,ax=-10,ay=0,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),
            go.layout.Annotation(x=0,y=y_upper,ax=0,ay=15,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),])

    fig = go.Figure(data=data,layout=layout)
    return fig

def DisplayTeamData(teamID):

    if teamID == 0:
        df = pd.read_csv('data/Team1Data.csv')
        # table_id = 'team1_table'
    elif teamID == 1:
        df = pd.read_csv('data/Team2Data.csv')
        # table_id = 'team2_table'
    elif teamID == 2:
        df = pd.read_csv('data/Team3Data.csv')
        # table_id = 'team3_table'
    
    NameTranslateTable = pd.read_excel('data/NameTranslateTable.xlsx').fillna('缺值')
    ENAME = NameTranslateTable.ENAME.tolist()
    CNAME = NameTranslateTable.CNAME.tolist()
    BD = [i[5:7]=='10' for i in df.ScrapDate.tolist()]
    df = df[BD]
    spe = list(set(df.Species))

    counts = []
    samples = []
    for s in spe:
        counts.append(sum(df[df.Species==s].Count))
        samples.append(len(df[df.Species==s]))
    
    tname = []
    for s in spe:
        if s in ENAME:
            if CNAME[ENAME.index(s)] != '缺值':
                tname.append(CNAME[ENAME.index(s)])
            else:
                tname.append(s)
        else:
            tname.append(s)

    odf = pd.DataFrame(dict(物種=tname,總數量=counts,清單數=samples))

    final_table = dash_table.DataTable(
        #id = table_id,
        data = odf.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in odf.columns],
        style_cell_conditional=[{'if': {'column_id': '物種'},'textAlign': 'left'}],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px',
                    'font-size':'12px',
                },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_table={
                    'height':'500px'
                }
    )


    return final_table


if __name__ == "__main__":        
    pass