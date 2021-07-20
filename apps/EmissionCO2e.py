import base64
import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scipy.stats as st
from dash.dependencies import Input, Output, State

import Librairie_2021
from app import app
from function import *

####################################
link = 'https://ressources.data.sncf.com/explore/dataset/emission-co2-tgv/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
df = pd.read_csv(link,
                 sep=';')

linreg = st.linregress(x=df['Distance (km)'],
                       y=df['TGV (1 pers.) - Empreinte CO2e (kgCO2e/voyageur)'])
x = df['Distance (km)'].apply([min, max])
distance = np.linspace(x['min'], x['max'], 200)
prediction = linreg.slope * distance + linreg.intercept

layout = html.Div([
    html.Br(),
    html.H4('Estimation du CO2e par voyageur', style={"textAlign": "center"}),
    dcc.Markdown('''
    Émissions de CO2e* (kgCO2e/voyageur) sur les principales liaisons TGV.

Estimation calculée de la manière suivante : distance du trajet x émission de CO2 par kilomètre d’un voyageur. La méthodologie utilisée par SNCF est conforme au guide méthodologique publié par l’État pour l’information CO2 des prestations de transport
    ''',
                 style={"textAlign": "center",
                        "font-size": "18px"}
                 ),
    html.Div(
        dbc.Row(
            id='CO2-dist-row',
            children=[
                dbc.Col(
                    dcc.Graph(
                        id='CO2-dist-graph',
                        style={'height': '80vh'},
                        figure={
                            'data': [
                                go.Scatter(
                                    x=df['Distance (km)'],
                                    y=df['TGV (1 pers.) - Empreinte CO2e (kgCO2e/voyageur)'],
                                    text=df['Liaison'],
                                    mode='markers',
                                    name='Données'
                                ),
                                go.Scatter(
                                    x=distance,
                                    y=prediction,
                                    text=df['Liaison'],
                                    mode='lines',
                                    name='Droite de regression'
                                )
                            ],
                            'layout': go.Layout(
                                title=' Empreinte CO2e with distance',
                                xaxis_tickfont_size=14,
                                yaxis=dict(
                                    title='Empreinte CO2e [kgCO2e/voyageur]',
                                    titlefont_size=16,
                                    tickfont_size=14,
                                ),
                                xaxis=dict(
                                    title='Distance[km]',
                                    titlefont_size=16,
                                    tickfont_size=14,
                                ),
                                legend=dict(
                                        x=0,
                                        y=1.0,
                                        bgcolor='rgba(255, 255, 255, 0)',
                                        bordercolor='rgba(255, 255, 255, 0)'
                                    )
                            )
                        }
                    ),
                    width={'size': 8, "offset": 2, 'order': 2}
                )
            ]
        )
    )
]
)
