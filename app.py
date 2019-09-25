# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 12:43:47 2019

@author: DB
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from textwrap import dedent

import dash_bootstrap_components as dbc
import visdcc
import time

from e_bird_utils import GetN_Species, GetTotalIndivisual,\
   GetN_Record, draw_bar, GetN_Participants, half_donut,\
   accumlate_people_trace

#################################################################
########################## APP SETUP ############################
#################################################################

external_scripts = [
    "https://code.jquery.com/jquery-3.4.1.min.js",
    ]

# themes from https://bootswatch.com/
app = dash.Dash(
    'E-bird dash',
     external_stylesheets=[dbc.themes.COSMO, "https://fonts.googleapis.com/css?family=Noto+Sans+TC|Noto+Serif&display=swap"],
     external_scripts=external_scripts,
     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},                
                {"content_type":"text/html"}]
     )

app.config.suppress_callback_exceptions = True
server = app.server

app.title = 'E-bird Taiwan'

# init figs

df = GetN_Species([2019,7,1], [2019,12,31])
fig_N_species = draw_bar(df.鳥種數.tolist(), df.觀察者.tolist())

df = GetTotalIndivisual([2019,7,1], [2019,12,31])
fig_TI_species = draw_bar(df.鳥總隻數.tolist(), df.觀察者.tolist())

df = GetN_Record([2019,7,1], [2019,12,31])
fig_Record_species = draw_bar(df.紀錄筆數.tolist(), df.觀察者.tolist())
nP = GetN_Participants([2019,7,1], [2019,12,31])
accP = f'累積參與人數: {nP}'


#####################################################################################
######################## LAYOUTs SECTION ##################################################
###################################################################


app.layout = app.layout = html.Div([
    visdcc.Run_js(id='javascript'),
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.A([html.Font('e', style={'color':'#4ca800'},className='EB'),html.Font('Bird',className='EB',style={'color':'#000000'}),html.Br(className="EB_sep"), html.Font(' Taiwan', style={'color':'#4ca800'})],style={'font-weight':'600'},className='logo_title navbar-brand',href="/"),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([
            html.Ul([
                html.Li(html.A('eBird Taiwan秋季大亂鬥', href='/Ebird%e7%a7%8b%e5%ad%a3%e6%8c%91%e6%88%b0%e8%b3%bd',className="NavLnks"),className="nav-item"),
                html.Li(html.A('關渡觀鳥大日', href='/%e9%97%9c%e6%b8%a1%e9%b3%a5%e5%8d%9a%e8%a7%80%e9%b3%a5%e5%a4%a7%e6%97%a5',className="NavLnks"),className="nav-item"),
                html.Li(html.A('全球觀鳥大日', href='https://ebird.org/taiwan/news/2019-ebird%E5%8D%81%E6%9C%88%E8%A7%80%E9%B3%A5%E5%A4%A7%E6%97%A5-10%E6%9C%8819%E6%97%A5',className="NavLnks"),className="nav-item"),
            ],className="navbar-nav mr-auto"),
            html.Img(src="assets/sponsor.png",height="71px",className="float-right"),
        ],id="navbar-collapse", navbar=True),
        ], className="navbar navbar-expand-md navbar-light bg-white justify-content-between"),
    html.Div(id='page-content'),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}),
    html.Div(id='js_out'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
    )
    
])

## 中文網址一定要事先encode才行!!  http://www.convertstring.com/zh_TW/EncodeDecode/UrlEncode
home_layout = html.Div([
    html.Hr(),
    html.Div(html.Iframe(srcDoc=open('assets/Logo.html','r',encoding='utf-8').read(),className="HomeBanner",id="HomeBanner"),className="ifwrap"),
    html.Div([
        html.Div("活動辦法", className="section_title"),
        html.Br(),
        dbc.CardDeck([
            dbc.Card([
                dbc.CardBody([
                    html.H2("eBird Taiwan秋季大亂鬥", className="card-title home-card-title"),
                    html.P("和其他eBirder組隊來PK，共有3隊任你選，ET灰面鵟鷹隊、ET黑面琵鷺隊、ET小辮鴴隊，在10月上傳最多觀察清單以及記錄到最多種鳥!",className="card-text home-card-content"),
                    html.Br(),html.Br(),html.Br(),
                ]),
                dbc.CardFooter(html.Div([
                        html.Div("2019/10/01-31",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-1", className="modal-entry border-0 bg-transparent")
                    ],className="d-flex align-items-center"), className="border-0 bg-transparent")
                ]),
            dbc.Card([
                dbc.CardBody([
                    html.H2("關渡觀鳥大日", className="card-title home-card-title"),
                    html.P("今年的關渡鳥博適逢eBird全球觀鳥大日，ebird Taiwan除了按照往例將在關渡鳥博設攤，另外在10/19觀鳥大日這天，特別邀請鳥友們前往鄰近關渡平原賞鳥、上傳紀錄。鳥友們請做好準備，一起來衝關渡觀鳥大日吧!",className="card-text home-card-content"),
                    html.Br(),html.Br(),html.Br(),
                ]),
                dbc.CardFooter(html.Div([
                        html.Div("2019/10/01-31",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-2", className="modal-entry border-0 bg-transparent")
                    ],className="d-flex align-items-center"), className="border-0 bg-transparent")
                ]),
            dbc.Card([
                dbc.CardBody([
                    html.H2("10/19十月觀鳥大日", className="card-title home-card-title"),
                    html.P("10月19日十月觀鳥大日(October Global Big Day)!去年的觀鳥大日集結全世界3萬多位eBirder的力量，短短24小時共記錄6,331種鳥類。台灣則記錄242種鳥類，送出372份清單，今年的結果究竟會如何?趕緊安排10月19日出門賞鳥，一起努力送清單吧!",className="card-text home-card-content"),
                    html.Br(),html.Br(),html.Br(),
                ]),
                dbc.CardFooter(html.Div([
                        html.Div("2019/10/01-31",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-3", className="modal-entry border-0 bg-transparent")
                    ],className="d-flex align-items-center"), className="border-0 bg-transparent")
                ]),           
        ], className="home-card-deck"),
        html.Br(),
        html.Br(),
        html.Div([
            html.Img(src="assets/chick.png",className="chick-img"),
            html.Div("完成任一活動之參賽者即可參加抽獎, 豐富大獎得主就是你啦！",className="home-footer"),
            html.Img(src="assets/chick.png",className="chick-img", style={"transform": "scaleX(-1)"}),
            ], className="d-flex justify-content-around align-items-center"),
        html.Br(),        
    ],id='move_up'),
    dbc.Modal([
        dbc.ModalHeader("eBird Taiwan秋季大亂鬥",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        ## Contents are not checked yet ##
        * 挑戰時間：2019.10.01-2019.10.31
        * 挑戰方式：
            * 在10/15之前填寫要加入的隊伍及至少上傳一份記錄清單，每人只能加入一隊，不能更換隊伍。
            * 清單上傳時請分享到隊伍帳號（ET灰面鵟鷹隊、ET黑面琵鷺隊、ET小辮鴴隊)，才能列入挑戰紀錄，需在10/31前完成分享。
            * 紀錄清單必須持續時間超過3分鐘，鳥種數量沒有以「X」代替的完整紀錄清單。
            * 賞鳥動態和eBird鳥訊快報需設為公開，才能列入紀錄。        
        * 獎項：
            * 記錄鳥種數最多或上傳紀錄清單最多的隊伍，全隊隊員可各獲得一次望遠鏡(歐帝生光學BRITEC R 10X42雙筒望遠鏡)抽獎機會。  
        * 得獎名單公布：
            * 2019.11.24, 於eBird Taiwan FB社團進行直播抽獎，公布得獎名單。
        
        ''')),className="modal-body"),
        dbc.ModalFooter(dbc.Button("關閉", id="close-modal-1", className="ml-auto")),
        ],id="modal-1",size="xl",centered=True),
    dbc.Modal([
        dbc.ModalHeader("關渡觀鳥大日",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        ## Contents are not checked yet ##
        * 挑戰時間：2019.10.19, 0:00-24:00
        * 挑戰方式：
            * 選擇活動範圍內就近熱點上傳紀錄清單，清單種類不限，但必須設為公開。
            * 所有紀錄都要在10月20日中午12:00前上傳到eBird，才能被計算在關渡觀鳥大日的統計結果裡。
        * 獎項：
            * 上傳鳥種數最多  
            * 上傳清單數最多
            * 上傳鳥隻數最多
        * 獎項：
            * 貓頭鷹浴巾組 _八色鳥咖啡出品*1
            * 歐帝生2019望遠鏡新品5折折價卷*1
        * 得獎名單公布：2019.10.20, 15:00於關渡鳥博eBird攤位公布
        ''')),className="modal-body"),
        dbc.ModalFooter(dbc.Button("關閉", id="close-modal-2", className="ml-auto")),
        ],id="modal-2",size="xl",centered=True),
    dbc.Modal([
        dbc.ModalHeader("10/19十月觀鳥大日",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        ## Contents are not checked yet ##
        * 挑戰時間：2019.10.19
        * 挑戰方式：
            * 在十月觀鳥大日完成一份鳥種數量沒有以「X」代替的完整紀錄清單。        
        * 獎項：
            * 望遠鏡(歐帝生光學BRITEC R 10X42雙筒望遠鏡)抽獎機會 
        * 得獎名單公布：
            * 2019.11.24, 於eBird Taiwan FB社團進行直播抽獎，公布得獎名單。
        ''')),className="modal-body"),
        dbc.ModalFooter(dbc.Button("關閉", id="close-modal-3", className="ml-auto")),
        ],id="modal-3",size="xl",centered=True),
    ]
    )

app1_layout = dbc.Container([        
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
        ], style={"box-shadow":"4px 4px 0px rgba(187, 187, 187, 0.25)"}, body=True, color="light"),
        html.Br(),
        ],fluid=True)


app2_layout = html.Div([
    html.Div("當前戰況", className="section_title"),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='donut1',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center"),
        dbc.Col(dcc.Graph(id='donut2',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center"),
        dbc.Col(dcc.Graph(id='donut3',config=dict(displayModeBar=False),className="half_donut"),xl = 4,lg = 4, md = 12, className = "d-flex justify-content-center")
    ]),
    html.Div(style={"padding":"80px"}),
    dbc.Row(dcc.Graph(figure=accumlate_people_trace()),className="d-flex justify-content-center"),
    html.Br(),
    ])

##########################################################################################
##########################################  CALLBACKs SECTION  ##########################
###########################################################################################

### for all pages ####
@app.callback(
    Output('javascript', 'run'),
    [Input('page-content', 'children')])
def resize(_): 
    return """
    function getWindowSize(){
        var w = $(window).width();
            setProps({
            'event':{'w':w}
            })
    }
    window.addEventListener("resize", getWindowSize);
    window.dispatchEvent(new Event('resize'));
    window.removeEventListener("resize", getWindowSize);
    """


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


### for home page
@app.callback(
    Output("modal-1", "is_open"),
    [Input("modal-entry-1", "n_clicks"), Input("close-modal-1", "n_clicks")],
    [State("modal-1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-2", "is_open"),
    [Input("modal-entry-2", "n_clicks"), Input("close-modal-2", "n_clicks")],
    [State("modal-2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-3", "is_open"),
    [Input("modal-entry-3", "n_clicks"), Input("close-modal-3", "n_clicks")],
    [State("modal-3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

### for 關渡觀鳥大日
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


### for autumn page
@app.callback(
    [Output('donut1', 'figure'),
    Output('donut2', 'figure'),
    Output('donut3', 'figure')],
    [Input('javascript', 'event')])
def set_donut_by_viewport_width(prop):  
    # I'll add get data from file functions here
    w = prop['w']
    fig1 = half_donut(105,100,0, w)
    fig2 = half_donut(179,148,1, w)
    fig3 = half_donut(452,790,2, w)
    return fig1, fig2, fig3

### for url setup
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
