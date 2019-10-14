# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
from textwrap import dedent

import dash_bootstrap_components as dbc
import visdcc

import pandas as pd
import flask

import datetime
import time

from apps import Home, AutumnChallenge, BigDayChallenge, NotYet, Admin
from setting import app


server = app.server


app.layout = html.Div([
    visdcc.Run_js(id='javascript'),
    dcc.Location(id='url', refresh=False),
    html.Nav([html.A([html.Font('e', style={'color':'#4ca800'},className='EB'),html.Font('Bird',className='EB',style={'color':'#000000'}),html.Br(className="EB_sep"), html.Font(' Taiwan', style={'color':'#4ca800'})],style={'font-weight':'600'},className='logo_title navbar-brand',href="/"),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([html.Ul([html.Li(html.A('秋季大亂鬥', href='/big-month-challenge',className="NavLnks"),className="nav-item"),
                html.Li(html.A('關渡觀鳥大日', href='/big-day-challenge',className="NavLnks"),className="nav-item"),
                html.Li(html.A('十月觀鳥大日', href='https://ebird.org/taiwan/news/2019-ebird%E5%8D%81%E6%9C%88%E8%A7%80%E9%B3%A5%E5%A4%A7%E6%97%A5-10%E6%9C%8819%E6%97%A5',className="NavLnks"),className="nav-item"),],className="navbar-nav mr-auto"),
            html.Img(src="assets/sponsor.png",height="51px",className="float-right"),],id="navbar-collapse", navbar=True),], className="navbar navbar-expand-md navbar-light bg-white justify-content-between"),
    html.Div(id='page-content'),      
    ])



@app.callback(Output('javascript', 'run'),
    [Input('page-content', 'children')])
def resize(_): 
    return """
    function getWindowSize(){
        var w = $(window).width();
            setProps({
            'event':{'w':w}
            })
    }
    function RenameFilterPlaceholder(){
        var x = document.getElementsByTagName("Input");
        if (x.length === 0) {console.log('so bad...');}
        for (var i = 0; i < x.length; i++) {
            if (x[i].placeholder === "filter data..."){
                console.log('condition met');
                x[i].placeholder = "篩選資料";
            }
        } 
    }

    window.addEventListener("resize", getWindowSize);
    window.addEventListener("resize", RenameFilterPlaceholder);
    window.dispatchEvent(new Event('resize'));
    window.removeEventListener("resize", getWindowSize);
    """


@app.callback(Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

### for url setup
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/big-day-challenge':
        if datetime.datetime.now() < datetime.datetime(2019, 10, 9):
            return NotYet.Not_yet_layout
        else:
            return BigDayChallenge.BigDay_layout
    elif pathname == '/big-month-challenge':
        return AutumnChallenge.Autumn_layout
    elif pathname == '/':
        return Home.home_layout
    elif pathname == '/SignUp':
        return AutumnChallenge.join_layout
    elif pathname == '/welcome': 
        return AutumnChallenge.joined_layout
    elif pathname == '/help':
        return AutumnChallenge.help_layout
    elif pathname == '/big-month-challenge-data':
        return AutumnChallenge.data_layout
    elif pathname == '/admin':
        return Admin.admin_layout




if __name__ == '__main__':
    app.run_server(debug=True)