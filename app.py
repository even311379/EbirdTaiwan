# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 12:43:47 2019

@author: DB
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import visdcc

import time

from e_bird_utils import GetN_Species, GetTotalIndivisual,\
   GetN_Record, draw_bar, GetN_Participants


# themes from https://bootswatch.com/

external_scripts = [
    "https://code.jquery.com/jquery-3.4.1.min.js",
    ]

app = dash.Dash(
    'E-bird dash',
     external_stylesheets=[dbc.themes.COSMO, "https://fonts.googleapis.com/css?family=Noto+Sans+TC|Noto+Serif&display=swap"],
     external_scripts=external_scripts,
     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},
                #{"http-equiv":"cache-control","content":"no-cache"},
                #{"http-equiv":"expires","content":"0"},
                {"content_type":"text/html"}]
     )

app.config.suppress_callback_exceptions = True
server = app.server

#app.title = 'E-bird dash'


df = GetN_Species([2019,7,1], [2019,12,31])
fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist())

df = GetTotalIndivisual([2019,7,1], [2019,12,31])
fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist())

df = GetN_Record([2019,7,1], [2019,12,31])
fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist())
nP = GetN_Participants([2019,7,1], [2019,12,31])
accP = f'累積參與人數: {nP}'






app.layout = app.layout = html.Div([
    visdcc.Run_js(id='javascript'),
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.A([html.Font('e', style={'color':'#4ca800'},className='EB'),html.Font('Bird',className='EB',style={'color':'#000000'}), html.Font(' Taiwan', style={'color':'#4ca800'})],style={'font-weight':'600'},className='logo_title navbar-brand',href="/"),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([
            html.Ul([
                html.Li(html.A('eBird Taiwan秋季大亂鬥', href='/Ebird%e7%a7%8b%e5%ad%a3%e6%8c%91%e6%88%b0%e8%b3%bd',className="NavLnks"),className="nav-item"),
                html.Li(html.A('關渡觀鳥大日', href='/%e9%97%9c%e6%b8%a1%e9%b3%a5%e5%8d%9a%e8%a7%80%e9%b3%a5%e5%a4%a7%e6%97%a5',className="NavLnks"),className="nav-item"),
                html.Li(html.A('全球觀鳥大日', href='https://ebird.org/octoberbigday',className="NavLnks"),className="nav-item"),
            ],className="navbar-nav mr-auto"),
            html.Img(src="assets/sponsor.png",height="71px",className="float-right"),
        ],id="navbar-collapse", navbar=True),
        ], className="navbar navbar-expand-md navbar-light bg-white justify-content-between"),
    html.Div(id='page-content'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
    )
    
])

## 中文網址一定要事先encode才行!!  http://www.convertstring.com/zh_TW/EncodeDecode/UrlEncode
home_layout = html.Div([
    html.Hr(),
    html.Iframe(srcDoc=open('assets/Logo.html','r',encoding='utf-8').read(),className="HomeBanner",id="HomeBanner"),
    html.Div([
        html.Hr(),
        html.H1('TESTEST',className='test',id='test'),
        html.Br(),
        html.H1('TESTEST2'),
    ],id='move_up',style={}),
    ]
    )

app1_layout = html.Div(children = [
        #title
        dbc.Container([
        dbc.Row([
        dbc.Col(html.Div([html.Font('e', style={'color':'#4ca800'},className='EB'),html.Font('Bird',className='EB'), html.Font(' Taiwan', style={'color':'#4ca800'})],style={'font-weight':'600'}),className='logo_title',width=2,lg=4),
        dbc.Col(html.Div('2019年關渡鳥博觀鳥大日',className = 'activity_title text-nowrap'),lg=4,sm=6,width=8),
        dbc.Col(xl=2,lg=2,md=0),
        dbc.Col(html.Div(dbc.Badge(accP,id='accp', pill=True,className='my_badge')), width=2, className='badge_size'),
        ], className="banner d-flex", align='center', style={'backgroundColor':'white'}),
        # map
        dbc.Row([
            html.Iframe(id='map',srcDoc=open('my_map.html','r',encoding='utf8').read(),className='my_map'),
            html.Div(dbc.Badge(accP,id='accp_o', pill=True, className='badge_overlay'))
        ]),
        html.Br(),
        # result
        dbc.Card([
            dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div('上傳鳥種數排名',className='fig_title'),width=7),
                    dbc.Col(html.Div('1小時前更新',id='ut1',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
                    ],justify='end',align='baseline'),
                html.Hr(),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=fig_N_species, id='fNs',config=dict(displayModeBar=False),className='my_fig'))),
                html.Hr(),
                ], xl=4,lg=4,md=12),
             dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div('上傳鳥隻數排名',className='fig_title'),width=7),
                    dbc.Col(html.Div('1小時前更新',id='ut2',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
                    ],justify='end',align='baseline'),
                html.Hr(),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=fig_TI_species, id='fTIs', config=dict(displayModeBar=False),className='my_fig'))),
                html.Hr(),
                ], xl=4,lg=4,md=12),
             dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div('上傳清單數排名',className='fig_title'),width=7),
                    dbc.Col(html.Div('1小時前更新',id='ut3',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
                    ],justify='end',align='baseline'),
                html.Hr(),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=fig_Record_species, id='fRs', config=dict(displayModeBar=False),className='my_fig'))),
                html.Hr(),
                ], xl=4,lg=4,md=12),
            ]),
            ],body=True
        ),
        ],fluid=True, style={'backgroundColor':'#E2EDF3'})])


app2_layout = html.Div(
    html.H1('This is app2!'))

@app.callback(
    Output('javascript', 'run'),
    [Input('page-content', 'children')])
def resize(_): 
    return "console.log('heyhey'); window.dispatchEvent(new Event('resize'));"


#@app.callback(
#    Output('javascript', 'run'),
#    [Input('fNs', 'figure')])
#def resize(_): 
#    return "console.log('resize'); window.dispatchEvent(new Event('resize'));"

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback([
    Output('accp', 'children'),
    Output('accp_o', 'children'),
    Output('ut1', 'children'),
    Output('ut2', 'children'),
    Output('ut3', 'children'),
    Output('fNs', 'figure'),
    Output('fTIs', 'figure'),
    Output('fRs', 'figure')],
    [Input('interval-component', 'n_intervals')],
    [State('accp', 'children'),
    State('fNs', 'figure'),
    State('fTIs', 'figure'),
    State('fRs', 'figure')],
    )
def update_all(n,s_accp,s_fNs,s_fTIs,s_fRs):
    if time.localtime().tm_min == 5:
        df = GetN_Species([2019,7,1], [2019,8,31])
        fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist())
        df = GetTotalIndivisual([2019,7,1], [2019,8,31])
        fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist())
        df = GetN_Record([2019,7,1], [2019,8,31])
        fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist())
        nP = GetN_Participants([2019,7,1], [2019,8,31])
        o_accp = f'累積參與人數: {nP}'
        s_ut1 = '1分鐘前更新'
        s_ut2 = '1分鐘前更新'
        s_ut3 = '1分鐘前更新'

        return o_accp, o_accp, s_ut1, s_ut2, s_ut3, fig_N_species, fig_TI_species, fig_Record_species
    else:
        m = time.localtime().tm_min
        s_ut1 = f'{m}分鐘前更新'
        s_ut2 = f'{m}分鐘前更新'
        s_ut3 = f'{m}分鐘前更新'
        return s_accp, s_accp, s_ut1, s_ut2, s_ut3, s_fNs, s_fTIs, s_fRs


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/%e9%97%9c%e6%b8%a1%e9%b3%a5%e5%8d%9a%e8%a7%80%e9%b3%a5%e5%a4%a7%e6%97%a5':
        return app1_layout
    elif pathname == '/Ebird%e7%a7%8b%e5%ad%a3%e6%8c%91%e6%88%b0%e8%b3%bd':
        return app2_layout
    elif pathname == '/':
        return home_layout


if __name__ == "__main__":
    app.run_server(debug=True)
