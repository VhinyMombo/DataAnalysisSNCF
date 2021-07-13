#### importation des modules ###############

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import scipy.stats
from dash.dependencies import Input, Output, State
from function import f_repartition
import dash_table
from app import app

#######################################################

annee = [*range(1851, 2021)]

##################################################################
layout = html.Div([
    html.Br(),
    html.H4('Select a range of years ', style={"textAlign": "center"}),
    html.Div(
        dbc.Row(
            dbc.Col(
                dcc.RangeSlider(id='DateSlider',
                                marks={annee[i]: str(annee[i]) for i in range(0, len(annee), 10)},
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
                                vertical=False,  # True, False - vertical, horizontal slider
                                verticalHeight=900,
                                included=True,
                                tooltip={'always_visible': False,
                                         'placement': 'bottom'}
                                ),
                width={'size': 8, "offset": 2, 'order': 1}
            )
        )
    ),
    html.Div(id='HistoTempsTravail', children=[])
]
)


@app.callback(
    Output('HistoTempsTravail', 'children'),
    [Input('DateSlider', 'value')],
    [State('HistoTempsTravail', 'children')]
)
def build_hist(years, divChildren):
    import numpy as np
    data = pd.read_csv(
        "https://ressources.data.sncf.com/explore/dataset/temps-de-travail-annuel-depuis-1851/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
        sep=";")
    df = data.query('Date >= ' + str(years[0]) + ' & Date <= ' + str(years[1])).sort_values('Date')
    x_years = df['Date']
    df2 = data[np.isnan(data["Temps annuel de travail (France)"]) == False]
    temps_france=df2["Temps annuel de travail (France)"]
    temps_sncf =df2['Temps annuel de travail (SNCF)']
    xsncf, tsncf = f_repartition(temps_sncf, n=60)
    xfr, tfr = f_repartition(temps_france, n=60)
    stat,pvalue = scipy.stats.ks_2samp(df2['Temps annuel de travail (SNCF)'],
                         df2['Temps annuel de travail (France)'])
    files = pd.DataFrame(data={'Statistique du test': stat, 'p-Value': pvalue},index=[0])

    divChildren = html.Div(
        children=[
            html.Br(),
            dbc.Row(id='bof',
                    children=[
                        dbc.Col(
                            dcc.Graph(
                                id="bar-plot",
                                style={'width': '80vh', 'height': '80vh'},
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
                                        xaxis=dict(
                                            title='Année',
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

                            ),
                            width={'size': 5, "offset": 1, 'order': 1}
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="cumulative-funct",
                                style={'width': '80vh', 'height': '80vh'},
                                figure={
                                    'data': [go.Scatter(y=tsncf, x=xsncf,
                                                        mode='lines',
                                                        name='SNCF',
                                                        marker_color='rgb(55, 83, 109)'),
                                             go.Scatter(y=tfr, x=xfr,
                                                        mode='lines',
                                                        name='France',
                                                        marker_color='rgb(26, 118, 255)',
                                                        )
                                             ],
                                    'layout': go.Layout(
                                        title='Fonction de Repartition du temps de Travail entre ' + str(
                                            min(df2['Date'])) + ' et ' + str(max(df2['Date'])),
                                        xaxis_tickfont_size=14,
                                        yaxis=dict(
                                            titlefont_size=16,
                                            tickfont_size=14,
                                        ),
                                        xaxis=dict(
                                            title='Heures',
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
                            width={'size': 5, 'offset': 0, 'order': 2}

                        )
                    ]
                    ),
            html.Br(),
            dbc.Col(
                html.Hr(),
                width={'size': 10, 'offset': 1, 'order': 1 }
            ),
            html.Br(),
            html.H2('Test de Kolmogorov - Smirnov', style={"textAlign": "center"}),
            html.Br(),
            dcc.Markdown('''
            On cherche à determiner si le temps de travail à la SNCF suit
            la même loi que le temps de travail en France. 
            
            De ce fait, il est plus interessant de les comparer à partir de
            1950, année à partir de laquelle, on a les données pour les 2 distributions
            
            Après avoir vu les fonctions de repartition (ci-dessus) des 2 distributions, il serait 
            interessant de regader l'allure de la fonction densité de probabilité.
            ''',
                         style={"textAlign": "center",
                                "font-size": "18px"}
                         ),
            dbc.Row(
                id='histo-test',
                children=[
                    dbc.Col(
                        dcc.Graph(
                            id="pdf_sncf",
                            style={'width': '80vh', 'height': '80vh'},
                            figure={
                                'data': [go.Histogram(
                                    x=temps_sncf,
                                    nbinsx=15,
                                    histnorm='probability',
                                    marker_color='rgb(55, 83, 109)',
                                    opacity=0.75)
                                ],
                                'layout': go.Layout(
                                    title=' PDF du temps de Travail (SNCF) entre ' + str(
                                        min(df2['Date'])) + ' et ' + str(max(df2['Date'])),
                                    xaxis_tickfont_size=14,
                                    yaxis=dict(
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    ),
                                    xaxis=dict(
                                        title='heures',
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    )
                                )
                            }
                        ),
                        width={'size': 5, 'offset': 1, 'order': 2}
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="pdf_fr",
                            style={'width': '80vh', 'height': '80vh'},
                            figure={
                                'data': [go.Histogram(
                                    x=temps_france,
                                    nbinsx=15,
                                    histnorm='probability',
                                    marker_color='rgb(26, 118, 255)',
                                    opacity=0.75)
                                ],
                                'layout': go.Layout(
                                    title=' PDF du temps de Travail (FRANCE) entre ' + str(
                                        min(df2['Date'])) + ' et ' + str(max(df2['Date'])),
                                    xaxis_tickfont_size=14,
                                    yaxis=dict(
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    ),
                                    xaxis=dict(
                                        title='heures',
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    )
                                )
                            }
                        ),
                        width={'size': 5, 'offset': 0, 'order': 2}
                    )
                ]
            ),
            html.Br(),
            dcc.Markdown('''
            **On essaie determiner si le temps de travail à la SNCF suit
            la même loi que le temps de travail en France.
            
            Soit l'hypothèse H0 : " le temps de travail à la SNCF et en France
            suivent la même loi", par le test KS on a :** 
            
            ''',
                         style={"textAlign": "center",
                                "font-size": "18px"}
                         ),
            html.Br(),
            dbc.Col(dash_table.DataTable(
                id='KS_table',
                columns=[{"name": i, "id": i} for i in ["Statistique du test", "p-Value"]],
                data=files.to_dict('records'),
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
                    'height': 'auto'
                }),
                width={'size': 4, "offset": 4, 'order': 1}
            ),
            html.Br(),
            html.Br(),
            dcc.Markdown('''
            Pour un risque alpha = 5 %, on a d_seuil = 0.1481. 
            
            La statistique du test étant nettement supérieure à d_seuil et la p_value étant 
            inférieure à 5% alors on rejette H0.

                ''',
                         style={"textAlign": "center",
                                "font-size": "18px"}
                         )

        ],
        style={'marginBottom': 50, 'marginTop': 25}
    )
    return divChildren
