#### importation des modules ###############

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from app import app

#######################################################

annee = [*range(1851, 2021)]

##################################################################
layout = dbc.Container((
    html.Br(),
    html.H4('Select a range of years ', style={"textAlign": "center"}),
    html.Div(
            dcc.RangeSlider(id='DateSlider',
                            marks={annee[i]: str(annee[i]) for i in range(0,len(annee),10)},
                            step=1,
                            min=min(annee),
                            max=max(annee),
                            value=[2006, 2017],
                            dots=False,
                            allowCross=False,
                            disabled=False,
                            pushable=1,
                            updatemode='mouseup',
                            className='None',
                            vertical=False,        # True, False - vertical, horizontal slider
                            verticalHeight=900,
                            included=True,
                            tooltip={'always_visible': False,
                                     'placement': 'bottom'}
                            )
    ),
    html.Div(id='HistoTempsTravail', children=[]),
),
    fluid=True
)


@app.callback(
    Output('HistoTempsTravail', 'children'),
    [Input('DateSlider', 'value')],
    [State('HistoTempsTravail', 'children')]
)
def build_hist(years, divChildren):
    data = pd.read_csv(
        "https://ressources.data.sncf.com/explore/dataset/temps-de-travail-annuel-depuis-1851/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
        sep=";")
    df = data.query('Date >= ' + str(years[0]) + ' & Date <= ' + str(years[1])).sort_values('Date')
    x_years = df['Date']
    divChildren = html.Div(
        children=[
            html.Br(),
            html.Br(),
            dbc.Row(
                dcc.Graph(
                    id="bar-plot",
                    style={'width': '180vh', 'height': '90vh'},
                    figure={
                        'data': [go.Bar(x=x_years,
                                        y=df['Temps annuel de travail (SNCF)'],
                                        name='SNCF',
                                        marker_color='rgb(55, 83, 109)'
                                        ),
                                 go.Bar(x=x_years,
                                        y=df['Temps annuel de travail (France)'],
                                        name='France',
                                        marker_color='rgb(26, 118, 255)'
                                        )
                                 ],
                        'layout': go.Layout(
                            title='Temps de Travail de ' + str(years[0]) + ' à ' + str(years[1]),
                            xaxis_tickfont_size=14,
                            yaxis=dict(
                                title='Heures',
                                titlefont_size=16,
                                tickfont_size=14,
                            ),
                            legend=dict(
                                x=0,
                                y=1.0,
                                bgcolor='rgba(255, 255, 255, 0)',
                                bordercolor='rgba(255, 255, 255, 0)'
                            ),
                            barmode='group',
                            bargap=0.15,  # gap between bars of adjacent location coordinates.
                            bargroupgap=0

                        )
                    }

                )
            )]
    )
    return divChildren
