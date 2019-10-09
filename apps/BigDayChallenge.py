# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import time
import datetime

from ebird_figs import GetN_Species, GetTotalIndivisual,\
   GetN_Record, draw_bar, GetN_Participants

from setting import app



# init figs
init_day = [2019,10,10]

df = GetN_Species(init_day, [2019,12,31])
fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(), 1300)

df = GetTotalIndivisual(init_day, [2019,12,31])
fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(), 1300)

df = GetN_Record(init_day, [2019,12,31])
fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(), 1300)
nP = GetN_Participants(init_day, [2019,12,31])
accP = f'累積參與人數: {nP}'


BigDay_layout = html.Div([
        dbc.Container([
        # map
        dbc.Row([html.Iframe(id='map',srcDoc=open('assets/my_map.html','r',encoding='utf8').read(),className='my_map'),
            html.Div(dbc.Badge(accP,id='accp_o', pill=True, className='badge_overlay'))]),
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
        dcc.Interval(id='interval-component',interval=60 * 1000, n_intervals=0),
    ])

first_draw_bar = True

### for 關渡觀鳥大日
@app.callback([Output('accp_o', 'children'),
    Output('ut1', 'children'),
    Output('ut2', 'children'),
    Output('ut3', 'children'),
    Output('fNs', 'figure'),
    Output('fTIs', 'figure'),
    Output('fRs', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('javascript', 'event')],
    [State('accp_o', 'children'),
    State('fNs', 'figure'),
    State('fTIs', 'figure'),
    State('fRs', 'figure')],)
def update_all(n, prop,s_accp,s_fNs,s_fTIs,s_fRs):
    
    global first_draw_bar

    if first_draw_bar:
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
            nP = GetN_Participants([2019,10,19], [2019,10,20])
        else:
            df = GetN_Species(init_day, [2019,12,31])
            fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(),w)
            df = GetTotalIndivisual(init_day, [2019,12,31])
            fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(),w)
            df = GetN_Record(init_day, [2019,12,31])
            fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(),w)
            nP = GetN_Participants(init_day, [2019,12,31])

        o_accp = f'累積參與人數: {nP}'
        s_ut1 = '1分鐘前更新'
        s_ut2 = '1分鐘前更新'
        s_ut3 = '1分鐘前更新'
        first_draw_bar = False
        return o_accp, s_ut1, s_ut2, s_ut3, fig_N_species, fig_TI_species, fig_Record_species

    if not prop:
        w = 1300
    else:
        w = prop['w']

    if time.localtime().tm_min == 0:
        if datetime.datetime.now() > datetime.datetime(2019,10,19):
            df = GetN_Species([2019,10,19], [2019,10,20])
            fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(),w)
            df = GetTotalIndivisual([2019,10,19], [2019,10,20])
            fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(),w)
            df = GetN_Record([2019,10,19], [2019,10,20])
            fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(),w)
            nP = GetN_Participants([2019,10,19], [2019,10,20])
        else:
            df = GetN_Species(init_day, [2019,12,31])
            fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist(),w)
            df = GetTotalIndivisual(init_day, [2019,12,31])
            fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist(),w)
            df = GetN_Record(init_day, [2019,12,31])
            fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist(),w)
            nP = GetN_Participants(init_day, [2019,12,31])
        o_accp = f'累積參與人數: {nP}'
        s_ut1 = '1分鐘前更新'
        s_ut2 = '1分鐘前更新'
        s_ut3 = '1分鐘前更新'

        return o_accp, s_ut1, s_ut2, s_ut3, fig_N_species, fig_TI_species, fig_Record_species
    else:
        m = time.localtime().tm_min
        s_ut1 = f'{m}分鐘前更新'
        s_ut2 = f'{m}分鐘前更新'
        s_ut3 = f'{m}分鐘前更新'
        return s_accp, s_ut1, s_ut2, s_ut3, s_fNs, s_fTIs, s_fRs

@app.callback(Output('data-range-hint','children'),
    [Input('interval-component', 'n_intervals')])
def Update_data_range_hint(n):
    if datetime.datetime.now() > datetime.datetime(2019,10,19):
        return '資料範圍: 2019/10/19 00:00 ~ 24:00'
    else:
        return '資料範圍: 2019/10/10 00:00 ~ 現在'