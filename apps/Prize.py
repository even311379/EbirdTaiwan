import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

Prize_layout = html.Div([
    html.Div("關渡觀鳥大日獎品", className="section_title"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div('參加獎',className='prize-title'),
            html.Div('eBird Taiwan 限量貼紙 & 2020台灣野鳥月曆',className='prize-text1'),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Img(src="assets/imgs/85X110mm-1.jpg",className='prize-img-owl'),width=4),
                dbc.Col(html.Img(src="assets/imgs/85X110mm-2.jpg",className='prize-img-owl'),width=4),
                dbc.Col(html.Img(src="assets/imgs/85X110mm-3.jpg",className='prize-img-owl'),width=4)
            ]),
            html.Br(),
            html.Img(src="assets/imgs/calender.png",className='prize-img-calender'),
            html.Div('凡是10/19在活動範圍內熱點上傳清單者，前來攤位(#54)出示上傳清單，即可獲得貼紙一份，並可參加2020台灣野鳥月曆抽獎，總共10個名額，先抽先贏喔!',className='prize-text2'),
        ],width=5,xl=5,xs=12),
        dbc.Col([
            html.Div('活動競賽獎品',className='prize-title'),
            html.Div('貓頭鷹浴巾組-八色鳥咖啡出品*1',className='prize-text5'),
            dbc.Card([
                html.Img(src='assets/imgs/owl.png',className='prize-img-owls'),
                html.Div('貓頭鷹浴巾組-八色鳥咖啡出品*1',className='prize-text3'),
            ],className='prize-card',body=True),
            html.Br(),
            dbc.Card([
                html.Img(src='assets/imgs/telescope_1.png',className='prize-tele1'),
                html.Div('歐帝生2019望遠鏡新品5折折價卷*1',className='prize-text4'),
                html.Img(src='assets/imgs/telescope_2.png',className='prize-tele2'),
            ],className='prize-card',body=True),
        ],width=7,xl=7,xs=12),
    ],className='prize-contents'),
    html.Br(),
    html.Div(style={"height": "100px", "background": "#84BC60"}),  


])