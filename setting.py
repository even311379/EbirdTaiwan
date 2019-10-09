import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# import flask

# from apps import Home, AutumnChallenge, BigDayChallenge, NotYet, Admin


external_scripts = ["/assets/jquery3.4.1.js",
                    "https://www.googletagmanager.com/gtag/js?id=UA-135756065-3",
                    "/assets/gtag.js"]

# themes from https://bootswatch.com/
app = dash.Dash('E-bird dash',
     external_stylesheets=[dbc.themes.COSMO, "https://fonts.googleapis.com/css?family=Noto+Sans+TC|Noto+Serif&display=swap"],
     external_scripts=external_scripts,
     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},                
                {"content_type":"text/html"}])


app.title = 'eBird Taiwan系列活動'
app.config.suppress_callback_exceptions = True
# def serve_layout():
#     if flask.has_request_context():
#         return master_layout
#     return html.Div([
#         master_layout,
#         Home.home_layout,
#         BigDayChallenge.BigDay_layout,
#         AutumnChallenge.Autumn_layout,
#         AutumnChallenge.join_layout,
#         AutumnChallenge.joined_layout,
#         AutumnChallenge.help_layout,
#         NotYet.Not_yet_layout,
#         Admin.admin_layout])


# app.layout = serve_layout