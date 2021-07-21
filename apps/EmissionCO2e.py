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
paramslinreg = pd.DataFrame(data={'a': (linreg.slope).round(4),
                                  'b': (linreg.intercept).round(4),
                                  'r squared': (linreg.rvalue**2).round(4),
                                  'p-value': (linreg.pvalue).round(4),
                                  'std error': (linreg.stderr).round(4)}, index=[0])

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
    ),
    dcc.Markdown('''
             l'equation de la droite de regression etant de la forme (D) : y = ax+b, l'estimation des paramètres a et b 
             
             est donnée par : 
            ''',
                 style={"textAlign": "center",
                        "font-size": "18px"}
                 ),
    dbc.Col(dash_table.DataTable(
        id='EstimationLinear_table',
        columns=[{"name": i, "id": i} for i in ["a",
                                                "b",
                                                "r squared",
                                                "p-value",
                                                "std error"]],
        data=paramslinreg.to_dict('records'),
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=7,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[  # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'fontWeight': 'bold'
        }),
        width={'size': 4, "offset": 4, 'order': 1}
    ),
    html.Br(),
    html.Br(),
    dcc.Markdown(
        '''
        Ce qui fait qu'en moyenne pour 1 km parcouru en TGV, un passager produit ''' + str((linreg.slope).round(4)) + '''
        kg de CO2
        ''',
        style={"textAlign": "center",
                        "font-size": "18px"}

    ),
    html.Br(),
    html.Br()

    ]
)
