# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import dash_bootstrap_components as dbc
import pandas as pd

from setting import app

team_cols = ['ScrapDate','Creator','Species','Count','DateTime','Hotspot','url','Duration']
ChallengeDay_cols = ['LocationID','Date','Observer','Species','Count','Link']

admin_layout = html.Div([
    html.Div('PWD? fill correct and contents will popup'),
    dcc.Input(id='PWD',debounce=True,type="password"),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1('SignUp Tables'),
        dash_table.DataTable(
            id='signup_table',
            columns=[{"name": i, "id": i} for i in ['ID','SignUpDate','Team']],
            data=pd.read_csv('data/SignUp.csv').to_dict('records'),
            export_format='csv',
            editable=True,
            filter_action='native',
            page_action='native',
            page_size= 50,
            row_deletable=True),
        dbc.Button('Add Row', id='editing-rows-button', n_clicks=0,color="success"),
        html.Br(),html.Br(),
        html.H3("SuperUser Auth required to SAVE edited data!"),
        dcc.Input(id='SuperPWD',debounce=True,type="password"),
        html.Br(),
        dbc.Button("*SAVE*", color="danger", id='SAVE-SignUp', n_clicks=0,style={'display':'none'}),
        html.P('',id='SAVE-SignUp-Result', style={'color':'red'}),
        html.Br(),html.Hr(),
        html.H1('Chanllenge Day Data'),
        html.Div(dash_table.DataTable(
            id='CD_table',
            columns=[{"name": i, "id": i} for i in ChallengeDay_cols],
            data=pd.read_csv('data/AllData.csv').to_dict('records'),
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_size= 200,
            export_format='csv',
        ),style={'height':'600px','overflow-y':'scroll'}),
        html.Br(),html.Hr(),
        html.H1('Autumn Challenge Data'),
        html.Br(),
        html.H2('ET黑面琵鷺隊'),
        html.Div(dash_table.DataTable(
            id='team1_table',
            columns=[{"name": i, "id": i} for i in team_cols],
            data=pd.read_csv('data/Team1Data.csv').to_dict('records'),
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_size= 100,
            export_format='csv',
        ),style={'height':'600px','overflow-y':'scroll'}),
        html.Br(),
        html.H2('ET灰面鵟鷹隊'),
        html.Div(dash_table.DataTable(
            id='team2_table',
            columns=[{"name": i, "id": i} for i in team_cols],
            data=pd.read_csv('data/Team2Data.csv').to_dict('records'),
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_size= 100,
            export_format='csv',
        ),style={'height':'600px','overflow-y':'scroll'}),
        html.Br(),
        html.H2('ET小辮鴴隊'),
        html.Div(dash_table.DataTable(
            id='team3_table',
            columns=[{"name": i, "id": i} for i in team_cols],
            data=pd.read_csv('data/Team3Data.csv').to_dict('records'),
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_size= 100,
            export_format='csv'
        ),style={'height':'600px','overflow-y':'scroll'}),
        html.Br(),html.Hr(),
        html.H1('Web Scraping Loggers:'),
        html.Br(),html.Br(),
        html.H2("Automation Chanllenge Day Log"),
        dcc.Markdown('',style={'height':'300px','overflow-y':'scroll'},id='log2'),
        html.Br(),html.Br(),
        html.H2("Automation Autumn Data Log"),
        dcc.Markdown('',style={'height':'300px','overflow-y':'scroll'},id='log1'),
        html.Br(),
    ],style={"display": "none"},id='admin-contents'),
    html.P(id='hiddenSignUp',style={'display':'none'}),
    html.Br(),
    html.Br(),
    ],className='container')


@app.callback(Output('admin-contents','style'),
              [Input('PWD','value')])
def check_admin_pwd(value):
    if value:
        if value == 'tesri':
            return {'display':'block'}
        else:
            return {'display':'none'}
    else:
        return {'display':'none'}

@app.callback(Output('SAVE-SignUp','style'),
              [Input('SuperPWD','value')])
def check_superadmin_pwd(value):
    if value:
        if value == 'even311379':
            return {'display':'block'}
        else:
            return {'display':'none'}
    else:
        return {'display':'none'}

@app.callback(
    [Output('signup_table', 'data'),
     Output('CD_table', 'data'),
     Output('team1_table', 'data'),
     Output('team2_table', 'data'),
     Output('team3_table', 'data'),
     Output('log1', 'children'),
     Output('log2', 'children')],
    [Input('editing-rows-button', 'n_clicks'),
     Input('javascript', 'event')],
    [State('signup_table', 'data')])
def add_SignUp_row(n_clicks, prop, rows):
    SignUpdata = pd.read_csv('data/SignUp.csv').to_dict('records')
    CDdata = pd.read_csv('data/AllData.csv').to_dict('records')
    T1data = pd.read_csv('data/Team1Data.csv').to_dict('records')
    T2data = pd.read_csv('data/Team2Data.csv').to_dict('records')
    T3data = pd.read_csv('data/Team3Data.csv').to_dict('records')
    with open('UpdateAutumnData.log','r',encoding='utf8') as f:
        log_text1 = f.read()
    with open('UpdateData.log','r',encoding='utf8') as f:
        log_text2 = f.read()

    if n_clicks > 0:
        rows.append({c['id']: '' for c in ['ID','SignUpDate','Team']})
        return rows,CDdata,T1data,T2data,T3data, log_text1, log_text2
    else:
        return SignUpdata,CDdata,T1data,T2data,T3data, log_text1, log_text2


@app.callback(
    Output('SAVE-SignUp-Result', 'children'),
    [Input('SAVE-SignUp', 'n_clicks')],
    [State('signup_table','data')])
def click_save_SignUp(n_clicks, table_data):
    if n_clicks > 0:
        saved = pd.DataFrame.from_records(table_data)
        saved.to_csv('data/SignUp.csv', index=False, encoding='utf-8')
        return 'File Saved'