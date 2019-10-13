import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from textwrap import dedent

from setting import app

home_layout = html.Div([html.Hr(),
    html.Div(html.Iframe(srcDoc=open('assets/logo.html','r',encoding='utf-8').read(),className="HomeBanner",id="HomeBanner"),className="ifwrap"),
    html.Div([html.Div("活動辦法", className="section_title"),
        html.Br(),
        dbc.CardDeck([dbc.Card([dbc.CardBody([html.H2("秋季大亂鬥", className="card-title home-card-title"),
                    html.P("想參加賞鳥比賽卻找不到隊友，又或者，時間總是無法配合?秋季大亂鬥就是最好的機會，讓你自由選擇隊伍，和全台eBirder組隊PK，還有一整個10月可上傳賞鳥紀錄。共有十月國慶鳥代表隊─ET灰面鵟鷹隊、來台度冬的貴客─ET黑面琵鷺隊、出沒在花生田的冬候鳥─ET小辮鴴隊等3隊，比比那隊最厲害，在10月上傳最多觀察清單以及記錄到最多種鳥!",className="card-text home-card-content"),
                    ]),
                dbc.CardFooter(html.Div([html.Div("2019/10/01-31",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-1", className="modal-entry border-0 bg-transparent")],className="d-flex align-items-center"), className="border-0 bg-transparent")]),
            dbc.Card([dbc.CardBody([html.H2("關渡觀鳥大日", className="card-title home-card-title"),
                    html.P("今年的關渡鳥博適逢eBird全球觀鳥大日，eBird Taiwan除了按照往例將在關渡鳥博設攤，另外在10/19觀鳥大日這天，特別邀請鳥友們前往鄰近關渡平原賞鳥、上傳紀錄。鳥友們請做好準備，一起來衝關渡觀鳥大日吧! ",className="card-text home-card-content"),
                    ]),
                dbc.CardFooter(html.Div([html.Div("2019/10/19",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-2", className="modal-entry border-0 bg-transparent")],className="d-flex align-items-center"), className="border-0 bg-transparent")]),
            dbc.Card([dbc.CardBody([html.H2("十月觀鳥大日", className="card-title home-card-title"),
                    html.P("10月19日是十月觀鳥大日(October Global Big Day)!去年的觀鳥大日集結全世界3萬多位eBirder的力量，短短24小時共記錄6,331種鳥類。台灣則記錄242種鳥類，送出372份清單，今年的結果究竟會如何?趕緊安排10月19日出門賞鳥，一起努力送清單吧!",className="card-text home-card-content"),
                    ]),
                dbc.CardFooter(html.Div([html.Div("2019/10/19",className="mr-auto date-range-text"),
                        dbc.Button("詳細活動說明",id="modal-entry-3", className="modal-entry border-0 bg-transparent")],className="d-flex align-items-center"), className="border-0 bg-transparent")]),], className="home-card-deck"),
        html.Br(),
        html.Br(),
        html.Div([html.Img(src="assets/chick.png",className="chick-img"),
            html.Div("完成任一活動之參賽者即可參加抽獎,豐富大獎得主就是你啦！",className="home-footer",id='FooterText'),
            html.Img(src="assets/chick.png",className="chick-img", style={"transform": "scaleX(-1)"}),], className="d-flex justify-content-around align-items-center"),
        html.Br(),],id='move_up'),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}),  
    dbc.Modal([dbc.ModalHeader("eBird Taiwan秋季大亂鬥",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        * 挑戰時間：2019.10.01-2019.10.31
        * 挑戰方式：
            * 在10/15之前填寫要加入的隊伍及至少上傳一份記錄清單，每人只能加入一隊，不能更換隊伍。
            * 清單上傳時請分享到隊伍帳號（ET灰面鵟鷹隊、ET黑面琵鷺隊、ET小辮鴴隊)，才能列入挑戰紀錄，需在10/31前完成分享。
            * 紀錄清單必須持續時間超過3分鐘，鳥種數量沒有以「X」代替的完整紀錄清單。
            * 賞鳥動態和eBird鳥訊快報需設為公開，才能列入紀錄。        
        * 獎項：
            * 記錄鳥種數最多或上傳紀錄清單最多的隊伍，全隊隊員可各獲得一次望遠鏡(歐帝生光學BRITEC R 10X42雙筒望遠鏡)抽獎機會。
        * 得獎名單公布
            * 2019.11.24，於eBird Taiwan FB 社團進行直播抽獎，公布得獎名單。
        ''')),className="modal-body"),
        dbc.ModalFooter([
            dbc.Button(html.A("活動連結",href='/big-month-challenge', style={'color':'white'}), className="ml-auto"),
            dbc.Button("關閉", id="close-modal-1")]),
    ],id="modal-1",size="xl",centered=True),       
    dbc.Modal([dbc.ModalHeader("關渡觀鳥大日",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        * 挑戰時間：2019.10.19, 0:00-24:00
        * 挑戰方式：
            * 選擇活動範圍內就近熱點上傳紀錄清單，清單種類不限，但必須設為公開。
            * 所有紀錄都要在10月20日中午12:00前上傳到eBird，才能被計算在關渡觀鳥大日的統計結果裡。
        * 獎項：
            * 上傳鳥種數最多  
            * 上傳清單數最多
            * 上傳鳥隻數最多
        * 獎品:三位得獎人將各獲得:
            * 貓頭鷹浴巾組-八色鳥咖啡出品*1
            * 歐帝生2019望遠鏡新品5折折價卷*1
        * 得獎名單公布：2019.10.20, 15:00於關渡鳥博eBird攤位公布

        ''')),className="modal-body"),
        dbc.ModalFooter([
            dbc.Button(html.A("活動連結",href='/big-day-challenge', style={'color':'white'}), className="ml-auto"),
            dbc.Button("關閉", id="close-modal-2")]),
    ],id="modal-2",size="xl",centered=True),
    dbc.Modal([dbc.ModalHeader("十月觀鳥大日",className="modal-title"),
        dbc.ModalBody(dcc.Markdown(dedent('''
        * 挑戰時間：2019.10.19
        * 挑戰方式：
            * 在十月觀鳥大日完成一份鳥種數量沒有以「X」代替的完整紀錄清單，可獲得一次望遠鏡(歐帝生光學BRITEC R 10X42雙筒望遠鏡)抽獎機會。
            * 所有紀錄需在10月23日前上傳到eBird，才能被計算在全球觀鳥大日的初步統計結果。
            * 參考：
                * [2018年觀鳥大日台灣紀錄](https://ebird.org/octoberbigday)
        * 獎項：
            * 望遠鏡(歐帝生光學BRITEC R 10X42雙筒望遠鏡)抽獎機會
        * 得獎名單公布：
            * 2019.11.24，於eBird Taiwan FB 社團進行直播抽獎，公布得獎名單。
        ''')),className="modal-body"),
        dbc.ModalFooter([
            dbc.Button(html.A("活動連結",href='https://reurl.cc/vnDLKl', style={'color':'white'}), className="ml-auto"),
            dbc.Button("關閉", id="close-modal-3")]),
    ],id="modal-3",size="xl",centered=True),
    ])


@app.callback(Output("modal-1", "is_open"),
    [Input("modal-entry-1", "n_clicks"), Input("close-modal-1", "n_clicks")],
    [State("modal-1", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output("modal-2", "is_open"),
    [Input("modal-entry-2", "n_clicks"), Input("close-modal-2", "n_clicks")],
    [State("modal-2", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output("modal-3", "is_open"),
    [Input("modal-entry-3", "n_clicks"), Input("close-modal-3", "n_clicks")],
    [State("modal-3", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open