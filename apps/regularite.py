import base64
import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import Librairie_2021
from app import app
from function import getData

####################################
dataset = ["regularite-mensuelle-intercites", "regularite-mensuelle-ter", "ponctualite-mensuelle-transilien"]
df = pd.DataFrame()
Statistiques = ["nombre d'observation",
                "minimum",
                "maximum",
                "moyenne empirique",
                "variance empirique",
                "skewness",
                "kurtosis"]
stats_name = ['mean', 'min', 'max', 'std', 'sum', 'median']
stats_py = [np.mean, min, max, np.std, np.sum, np.median]
#####################################

layout = dbc.Container((
    dcc.Markdown('''
    Follow the instruction for each dropdown! 
    '''),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='Dataset-Dropdown',
                             multi=False,
                             value=dataset[2],
                             placeholder='Select Dataset',
                             options=[{'label': c, 'value': c}
                                      for c in dataset]
                             ),
                width={'size': 4, "offset": 4, 'order': 1}
                )
    ]
    ),
    html.Div(id='container', children=[])

),
    fluid=True)


@app.callback(
    Output('container', 'children'),
    [Input('Dataset-Dropdown', 'value')],
    [State('container', 'children')]
)
def displays_graph(value, div_children):
    global df
    df = getData(value)
    dfobj = df.select_dtypes(include=object).columns
    new_child = html.Div(
        children=[
            html.Br(),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='filter-Dropdown',
                                     multi=False,
                                     value=dfobj[0],
                                     placeholder='Select a filter',
                                     options=[{'label': c, 'value': c}
                                              for c in dfobj]
                                     ),
                        width={'size': 4, 'offset': 1, 'order': 1}
                        ),
                dbc.Col(dcc.Dropdown(id='Stastitic-Dropdown',
                                     multi=False,
                                     value=stats_name[0],
                                     placeholder='Select a stastitic',
                                     options=[{'label': c, 'value': c}
                                              for c in stats_name]
                                     ),
                        width={'size': 4, 'offset': 2, 'order': 2}
                        )

            ]),
            html.Div(id='container2', children=[])
        ])
    div_children = new_child
    return new_child


@app.callback(Output('container2', 'children'),
              [Input('filter-Dropdown', 'value')],
              [State('container2', 'children')]
              )
def update_dropdown(First_filter, div_children2):
    div_children2 = html.Div(
        children=[
            html.Br(),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='Region-Dropdown',
                                     multi=False,
                                     value=df[First_filter][0],
                                     placeholder='Select ...',
                                     options=[{'label': c, 'value': c}
                                              for c in df[First_filter].unique()]
                                     ),
                        width={'size': 4, 'offset': 1, 'order': 1}
                        ),
                dbc.Col(dcc.Dropdown(id='categorie-Dropdown',
                                     multi=False,
                                     value=df.select_dtypes(include='float64').columns[0],
                                     placeholder='Select a category',
                                     options=[{'label': c, 'value': c}
                                              for c in df.select_dtypes(include='float64').columns]
                                     ),
                        width={'size': 4, 'offset': 2, 'order': 2}
                        )
            ]),
            html.Div(id='container3', children=[])
        ]
    )
    return div_children2


@app.callback(Output('container3', 'children'),
              [Input('categorie-Dropdown', 'value'),
               Input('Region-Dropdown', 'value'),
               Input('filter-Dropdown', 'value'),
               Input('Stastitic-Dropdown', 'value')],
              [State('container2', 'children')]
              )
def update_graphics(categorie, region, first_filter, stats, div_children3):
    data = df[df[first_filter] == region]
    valeur = [data[categorie].size,
              data[categorie].min(axis=0),
              data[categorie].max(axis=0),
              data[categorie].mean(axis=0),
              data[categorie].std(axis=0),
              data[categorie].skew(axis=0),
              data[categorie].kurtosis(axis=0)]
    files = pd.DataFrame(data={'Statistiques': Statistiques, 'Valeur': valeur})
    # create some matplotlib graph
    nom = 'image'
    dta = data[categorie]
    data2 = data.groupby('Date')[categorie].agg([np.mean, min, max, np.std, np.sum, np.median])
    df2 = df.groupby('Date')[categorie].agg([np.mean, min, max, np.std, np.sum, np.median])

    Librairie_2021.histo_Continue(dta.dropna(), 10, nom)
    aujourdhui = datetime.datetime.today()
    jour = "{}{}{}".format(aujourdhui.timetuple()[2], aujourdhui.timetuple()[1], aujourdhui.timetuple()[0])
    nom_fig = "{}_histo_{}.png".format(nom, jour)
    test_base64 = base64.b64encode(open(nom_fig, 'rb').read()).decode('ascii')
    div_children3 = html.Div(
        children=[
            html.Br(),
            html.Hr(),
            dbc.Row([
                dbc.Col(dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in ["Statistiques", "Valeur"]],
                    data=files.to_dict('records'),
                    editable=True,  # allow editing of data inside all cells
                    filter_action="native",  # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                    sort_mode="single",  # sort across 'multi' or 'single' columns
                    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                    row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                    row_deletable=True,  # choose if user can delete a row (True) or not (False)
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
                    width={'size': 4, "offset": 1, 'order': 1}
                ),
                dbc.Col(html.Img(id='Image',
                                 src='data:image/png;base64,{}'.format(test_base64),
                                 style={'height': '95%', 'width': '100%'}),
                        width={'size': 4, "offset": 1, 'order': 2}
                        )
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="scatter_chart",
                                  figure={
                                      'data': [go.Scatter(
                                          x=data2.index,
                                          y=data2[stats])],
                                      'layout': go.Layout(
                                          title={
                                              'text': categorie + " <br> (en " + stats + ")  pour " + region,
                                              'y': 0.9,
                                              'x': 0.5,
                                              'xanchor': 'center',
                                              'yanchor': 'top'
                                          },
                                          xaxis={
                                              'title': 'date'
                                          },
                                          yaxis={
                                              'title': categorie
                                          }
                                      )
                                  }
                                  ),
                        width={'size': 4, "offset": 1, 'order': 1}
                        ),
                dbc.Col(dcc.Graph('scatter_chart2',
                                  figure={
                                      'data': [go.Scatter(
                                          x=df2.index,
                                          y=df2[stats])],
                                      'layout': go.Layout(
                                          title={
                                              'text': categorie + " <br> (en " + stats + ")  pour tous les " + first_filter,
                                              'y': 0.9,
                                              'x': 0.5,
                                              'xanchor': 'center',
                                              'yanchor': 'top'
                                          },
                                          xaxis={
                                              'title': 'date'
                                          },
                                          yaxis={
                                              'title': categorie
                                          }
                                      )
                                  }
                                  ),
                        width={'size': 4, "offset": 1, 'order': 2}
                        )

            ])

        ]

    )
    return div_children3
