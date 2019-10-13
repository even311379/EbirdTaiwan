# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import time
import datetime

from ebird_figs import GetN_Species, GetTotalIndivisual,\
   GetN_Record, draw_bar, GetN_Participants, Get_All_N_List, Get_All_N_Species

from setting import app



# init figs
init_day = [2019,10,10]

df = GetN_Species(init_day, [2019,12,31])
fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(), 1300)

df = GetTotalIndivisual(init_day, [2019,12,31])
fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(), 1300)

df = GetN_Record(init_day, [2019,12,31])
fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(), 1300)

nS = Get_All_N_Species(init_day, [2019,12,31])
nL = Get_All_N_List(init_day, [2019,12,31])
nP = GetN_Participants(init_day, [2019,12,31])



BigDay_layout = html.Div([
        dbc.Container([
        # map
        dbc.Row([
            html.Iframe(id='map',srcDoc=open('assets/my_map.html','r',encoding='utf8').read(),className='my_map'),
            html.Div([
                html.Div([
                dbc.Row([dbc.Col('總鳥種數',width=9),dbc.Col(str(nS),width=2,id='accb',className='d-flex justify-content-center')],className='info-item'),
                dbc.Row([dbc.Col('累積上傳清單',width=9),dbc.Col(str(nL),width=2,id='accl',className='d-flex justify-content-center')],className='info-item'),
                dbc.Row([dbc.Col('累積參與人數',width=9),dbc.Col(str(nP),width=2,id='accp',className='d-flex justify-content-center')],className='info-item'),
                ]),
            ],className='info-overlay'),
        ]),
        html.Br(),
        # result
        dbc.Card([dbc.Row([dbc.Col([dbc.Row([dbc.Col(html.Div('上傳鳥種數排名',className='fig_title'),width=7),
                        dbc.Col(html.Div('1小時前更新',id='ut1',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),],justify='end',align='baseline'),
                    html.Hr(),
                    dbc.Row(dbc.Col(dcc.Graph(figure=fig_N_species, id='fNs',config=dict(displayModeBar=False),className='my_fig'))),
                    html.Hr(),], xl=4,lg=4,md=12),
                dbc.Col([dbc.Row([dbc.Col(html.Div('上傳鳥隻數排名',className='fig_title'),width=7),
                        dbc.Col(html.Div('1小時前更新',id='ut2',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),],justify='end',align='baseline'),
                    html.Hr(),
                    dbc.Row(dbc.Col(dcc.Graph(figure=fig_TI_species, id='fTIs', config=dict(displayModeBar=False),className='my_fig'))),
                    html.Hr(),], xl=4,lg=4,md=12),
                dbc.Col([dbc.Row([dbc.Col(html.Div('上傳清單數排名',className='fig_title'),width=7),
                        dbc.Col(html.Div('1小時前更新',id='ut3',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),],justify='end',align='baseline'),
                    html.Hr(),
                    dbc.Row(dbc.Col(dcc.Graph(figure=fig_Record_species, id='fRs', config=dict(displayModeBar=False),className='my_fig'))),
                    html.Hr(),], xl=4,lg=4,md=12),]),], style={"box-shadow":"4px 4px 0px rgba(187, 187, 187, 0.25)"}, body=True, color="light"),
        html.Br(),
        html.P('資料範圍: 2019/10/10 00:00 ~ 現在',style={'text-align':'right','paddning-right':'30px'}, id='data-range-hint',className='text-muted'),
        html.Br(),
        ],fluid=True),
        html.Div(style={"height": "100px", "background": "#84BC60"}), 
    ])



### for 關渡觀鳥大日
@app.callback([
    Output('accb', 'children'),
    Output('accl', 'children'),
    Output('accp', 'children'),
    Output('ut1', 'children'),
    Output('ut2', 'children'),
    Output('ut3', 'children'),
    Output('fNs', 'figure'),
    Output('fTIs', 'figure'),
    Output('fRs', 'figure')],
    [Input('javascript', 'event')]
   )
def update_all(prop):

    time.sleep(1) # wait for js to run
    if not prop:
        w = 1300
    else:
        w = prop['w']

    if datetime.datetime.now() > datetime.datetime(2019,10,19):
        df = GetN_Species([2019,10,19], [2019,10,20])
        fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(),w)
        df = GetTotalIndivisual([2019,10,19], [2019,10,20])
        fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(),w)
        df = GetN_Record([2019,10,19], [2019,10,20])
        fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(),w)
        nS = Get_All_N_Species([2019,10,19], [2019,12,31])
        nL = Get_All_N_List([2019,10,19], [2019,12,31])
        nP = GetN_Participants([2019,10,19], [2019,10,20])
    else:
        df = GetN_Species(init_day, [2019,12,31])
        fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(),w)
        df = GetTotalIndivisual(init_day, [2019,12,31])
        fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(),w)
        df = GetN_Record(init_day, [2019,12,31])
        fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(),w)
        nS = Get_All_N_Species(init_day, [2019,12,31])
        nL = Get_All_N_List(init_day, [2019,12,31])
        nP = GetN_Participants(init_day, [2019,12,31])

    m = datetime.datetime.now().minute
    s_ut1 = f'{m}分鐘前更新'
    s_ut2 = f'{m}分鐘前更新'
    s_ut3 = f'{m}分鐘前更新'
    
    return str(nS),str(nL),str(nP), s_ut1, s_ut2, s_ut3, fig_N_species, fig_TI_species, fig_Record_species
    # return str(999),str(9),str(99), s_ut1, s_ut2, s_ut3, fig_N_species, fig_TI_species, fig_Record_species


@app.callback(Output('data-range-hint','children'),
    [Input('javascript', 'event')])
def Update_data_range_hint(n):
    if datetime.datetime.now() > datetime.datetime(2019,10,19):
        return '資料範圍: 2019/10/19 00:00 ~ 24:00'
    else:
        return '資料範圍: 2019/10/10 00:00 ~ 現在'