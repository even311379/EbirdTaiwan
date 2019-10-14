# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import visdcc

import flask
import pandas as pd
import time
import datetime


from ebird_figs import  setup_donuts,accumlate_people_trace,DisplayTeamData
from setting import app

init_donut1, init_donut2, init_donut3 = setup_donuts(1600, datetime.datetime(2019,10,1))

Autumn_layout = html.Div([
    html.Div("當前戰況", className="section_title"),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=init_donut1,id='donut1',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center"),
        dbc.Col(dcc.Graph(figure=init_donut2,id='donut2',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center"),
        dbc.Col(dcc.Graph(figure=init_donut3,id='donut3',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center")
        ]),
    html.Br(),    
    html.Br(),
    dcc.Link('我要加入', href='/SignUp',className='JoinBtn d-flex align-items-center justify-content-center',id='JoinBtn'),
    html.Br(),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}), 
    html.Div(id='join-submit',style={'display':'none'}), # hidden ids inorder to make this app correct
    html.Div(id='form-contents',style={'display':'none'}),
    html.Div(id='hint-text',style={'display':'none'}),
    dcc.Input(id='account-input',style={'display':'none'})
    ],id='app2_layout')

join_layout = html.Div([
    html.Div("活動報名", className="section_title"),
    dbc.Row([
        dbc.Col([
            html.Form([
            dbc.Row('eBird公開顯示名稱', className='align-items-center'),
            dbc.Row(dcc.Input(debounce=True,id='account-input', className='form-inputs',name='new_acct',required=True)),
            dbc.Row('選擇隊伍', className='align-items-center'),
            dbc.Row(dcc.Dropdown(options=[
                    dict(label='ET灰面鵟鷹隊',value='ET灰面鵟鷹隊'),
                    dict(label='ET黑面琵鷺隊',value='ET黑面琵鷺隊'),
                    dict(label='ET小辮鴴隊',value='ET小辮鴴隊'),],
                value='ET灰面鵟鷹隊',id='team-option', className='form-inputs d-flex align-items-center'), className='align-items-center'),
            dbc.Row(html.Div('',id='hint-text'), className='align-items-center'),
            dbc.Row(html.Button('提交並開始比賽!', type='submit',id='join-submit'), className='align-items-center'),
            dbc.Row([
                dcc.Link('忘記公開顯示帳號',href='/help',style={'color':'#37760E'}),
                html.Font('|',className='px-3',style={'color':'#37760E'}),
                html.A('創建新帳號',href='https://secure.birds.cornell.edu/cassso/account/create',style={'color':'#37760E'})
                ], className='mt-3 mx-auto help-lnks'),
            dcc.Input(id='team-output',name='team',style={'display':'none'}),
            ], action='/post', method='post'),
            ],lg=4, md = 12, className='d-flex justify-content-center signup-form-col'),
        dbc.Col(dcc.Graph(figure=accumlate_people_trace('2019-09-25',1250),id='team_accp',config=dict(displayModeBar=False)),lg=8,md = 12, className='d-flex justify-content-center'),
        ], className='form-contents'),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}), 
    ], id='form-contents')
    

joined_layout = html.Div([
    html.Div("選隊完成!", className="section_title"),
    html.Div(className='gap'),
    dbc.Row([
        dbc.Col(html.Img(src="assets/joined.svg",className='joined-fig'),lg=5,md=12),
        dbc.Col([html.P('請拿出望遠鏡出門賞鳥'),html.P('記得分享清單給你的隊伍!')],className='joined-info',lg=7,md=12),
        ],className='d-flex align-items-center'),
    html.Div(className='gap'),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}), 
    ])




help_layout = html.Div([
    html.Div(className='help-img'),
    html.Div(style={"height": "100px", "background": "#84BC60"})])


data_layout = html.Div([
    #visdcc.Run_js(id='javascript-rn'),
    html.Div("資料表", className="section_title"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H1('ET灰面鵟鷹隊',className='month-data-title'),
            html.Div(DisplayTeamData(0),className='month-data-table')
        ],xl = 4,lg = 4, md = 12),
        dbc.Col([
            html.H1('ET黑面琵鷺隊',className='month-data-title'),
            html.Div(DisplayTeamData(1),className='month-data-table')
        ],xl = 4,lg = 4, md = 12),
        dbc.Col([
            html.H1('ET小辮鴴隊',className='month-data-title'),
            html.Div(DisplayTeamData(2),className='month-data-table')
        ],xl = 4,lg = 4, md = 12),        
    ]),
    html.Br(),
    html.P("可在篩選資料欄位直接輸入篩選條件，如: '> 10' 或 '鷗'。",className='text-muted',style={'text-align':'right','padding-right':'30px','font-size':'12px'}),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}), 
])

@app.callback([Output('donut1', 'figure'),
    Output('donut2', 'figure'),
    Output('donut3', 'figure')],
    [Input('javascript', 'event')])
def set_donut_by_viewport_width(prop):      
    w = prop['w']
    fig1, fig2, fig3 = setup_donuts(w, datetime.datetime(2019,10,1))
    return fig1, fig2, fig3

account_is_used = False

@app.callback(Output('team_accp', 'figure'),
    [Input('javascript', 'event')])
def set_team_accp_fig(prop):
    global account_is_used
    account_is_used = False
    if not prop:
        return accumlate_people_trace('2019-09-27',1300)
    else:
        w = prop['w']
        return accumlate_people_trace('2019-09-27',w)



@app.callback([Output('account-input','style'),
    Output('hint-text','children'),
    Output('team-output','value')],
    [Input('account-input',"value"),
     Input('team-option','value')])
def check_account_not_duplicate(account, team_name):
    global account_is_used
    if account_is_used:
        return {'':''} , '帳號已經報名過囉~', team_name
    accounts = pd.read_csv('data/SignUp.csv')
    if account in accounts.ID.tolist():
        team = accounts[accounts.ID==account].Team.tolist()[0]
        return {'color':'red'}, f'已經報名過囉~ 你是{team}~', team_name
    else:
        return {'':''} , '' , team_name


@app.server.route('/post', methods=['POST'])
def on_post():
    data = flask.request.form
    accounts = pd.read_csv('data/SignUp.csv')
    global account_is_used
    if data['new_acct'] in accounts.ID.tolist():
        account_is_used = True
        return flask.redirect('/SignUp')
    else:
        account_is_used = False
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        ndf = accounts.append(pd.DataFrame(dict(ID=[data['new_acct']],Team=[data['team']],SignUpDate=[today])), ignore_index=True)
        ndf.to_csv('data/SignUp.csv',index=False)
        return flask.redirect('/welcome')