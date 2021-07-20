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
from function import *

####################################
dataset = ["regularite-mensuelle-intercites", "regularite-mensuelle-ter", "ponctualite-mensuelle-transilien",
           "regularite-mensuelle-tgv-aqst", "regularite-mensuelle-tgv-axes"]
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

# layout = dbc.Container((
layout = html.Div([
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
    dcc.Markdown(id='Dataset-markdown',
                 children=[],
                 style={"textAlign": "center",
                        "font-size": "18px"},
                 ),
    html.Div(id='container', children=[])

]),


#    fluid=True)

@app.callback(
    Output('Dataset-markdown','children'),
    [Input('Dataset-Dropdown', 'value')]
)

def update_markdown_dataset(Dataset):
    if Dataset == "regularite-mensuelle-intercites":
        return '''
        Régularité mensuelle des trains Intercités de jour depuis janvier 2014.

Sur Intercités, la régularité est calculée lors de l’arrivée du train à la dernière gare de son parcours (terminus). Ce mode de calcul, qui n’intègre pas les gares intermédiaires, propose le retard cumulé sur l’ensemble d’un trajet.

L’indicateur utilisé est celui de la « régularité composite » : un train est considéré en retard s’il arrive cinq minutes après son heure prévue pour un trajet de moins de 1h30, dix minutes pour un trajet de 1h30 à 3h, et quinze minutes pour un trajet de plus de 3h.

Un train supprimé avant 16h la veille de sa circulation ne sera pas comptabilisé. En revanche, si l’annonce de sa suppression n’a pu être faite la veille avant 16h, le train sera bien comptabilisé comme un train supprimé, que cette suppression soit totale ou partielle (le train a effectué qu’une partie de son parcours). Par ailleurs, des trains Intercités peuvent effectuer une partie importante de leur trajet sous service TER. Ils sont alors comptabilisés dans les données de régularité TER.

Le calcul de la régularité Intercités proposé ici ne prend pas en compte la totalité des trains, mais une sélection déterminée par l’Autorité de la Qualité de Service dans les Transports (AQST).
        '''
    elif Dataset == "regularite-mensuelle-ter":
        return '''
        Régularité mensuelle TER depuis janvier 2013.

Sur TER, la régularité est calculée lors de l’arrivée du train à la dernière gare de son parcours (terminus). Ce mode de calcul, qui n’intègre pas les gares intermédiaires, propose le retard cumulé sur l’ensemble d’un trajet.

L’indicateur utilisé est celui de la « régularité à cinq minutes » : un train est considéré en retard s’il arrive cinq minutes après son heure prévue. Les données proposées ne sont pas détaillées par ligne TER mais agrégées pour tous les TER d’une Région.

En accord avec les Régions qui sont les autorités organisatrices des transports pour TER, un train supprimé avant 16h la veille de sa circulation ne sera pas comptabilisé. En revanche, si l’annonce de sa suppression n’a pu être faite la veille avant 16h, le train sera bien comptabilisé comme un train supprimé, que cette suppression soit totale ou partielle (le train a effectué qu’une partie de son parcours).
        
        '''
    elif Dataset == "ponctualite-mensuelle-transilien":
        return '''
        Ponctualité mensuelle Transilien depuis janvier 2013.

Sur Transilien, la qualité de service est évaluée au regard de la "ponctualité voyageurs", c’est-à-dire le pourcentage de voyageurs arrivant avec un retard de moins de cinq minutes à leur gare de destination.

Depuis janvier 2002, en accord avec Île-de-France Mobilités (IDFM) - anciennement Syndicat des transports d’Ile-de-France (STIF) - qui est l’autorité organisatrice des transports pour Transilien, le mode de calcul ne s’effectue plus sur la base du nombre de trains mais du nombre de voyageurs impactés. L’objectif est de refléter la réalité du parcours de chaque voyageur. Pour chaque train supprimé ou retardé de plus de cinq minutes, il est donc possible de connaître le nombre de voyageurs qui sont impactés par une perturbation. 

Pour réaliser ce calcul, des agents mandatés par IDFM et Transilien réalisent des comptages permettant de connaître le nombre d’entrants et de descendants dans les gares, et cela pour tous les trains au cours de la semaine. Ces données sont actualisées en fonction des données transmises par les portiques de contrôle.
        '''
    elif Dataset == "regularite-mensuelle-tgv-aqst":
        return '''
        Découvrez la régularité mensuelle TGV par liaisons (AQST).

La régularité TGV tient compte des différentes durées de trajet des clients (aussi appelée composite).

Les horaires d'arrivée sont également déterminés par des capteurs détectant le passage du train à un point déterminé marquant l'entrée en gare et exceptionnellement par des suivis manuel. La précision des mesures est la minute arrondie à minute inférieure, ce qui est conforme à l'ensemble des normes retenues pour la confection des horaires et chronogrammes de service.
Le résultat de régularité global n’est ni la moyenne des résultats des 6 axes, ni la moyenne des résultats de l’ensemble des liaisons. En effet, le taux de régularité est le nombre de trains à l’heure à leur terminus sur le nombre de trains total ayant circulé sur le périmètre considéré. De plus, un même TGV peut compter dans plusieurs liaisons, mais il ne compte qu’une seule fois dans la régularité globale. 
        '''
    elif Dataset == "regularite-mensuelle-tgv-axes":
        return '''
        Découvrez la régularité mensuelle des grands axes TGV.

La régularité TGV tient compte des différentes durées de trajet des clients (aussi appelée composite).

Le 4 secteurs géographiques TGV correspondent aux quatre gares TGV parisiennes. TGV International regroupent les trains internationaux de SNCF (SVI, ALLEO, LYRIA, ELIPSOS). Les trains opérés par d'autres entreprises ferroviaires comme Thalys et Eurostar ne sont pas pris en compte.
        '''



@app.callback(
    Output('container', 'children'),
    [Input('Dataset-Dropdown', 'value')],
    [State('container', 'children')]
)
def displays_graph(value, div_children):
    global df
    dff = getData(value)
    df = dff
    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').fillna('Autres')
    dfobj = df.select_dtypes(include=object).columns
    xdf = df[dfobj[0]].unique()
    xdf = xdf[~pd.isnull(xdf)]
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
            html.Hr(),
            dbc.Row((
                dbc.Col(
                    id="dbc_Region-Dropdown",
                    children=[
                        dcc.Dropdown(
                            id='Region-Dropdown',
                            value=xdf[0],
                            multi=False,
                            placeholder='Select ...',
                            options=[]
                        )
                    ],
                    width={'size': 4, 'offset': 1, 'order': 1}
                ),
                dbc.Col(
                    dcc.Dropdown(id='categorie-Dropdown',
                                 multi=False,
                                 value=df.select_dtypes(include='float64').columns[0],
                                 placeholder='Select a category',
                                 options=[{'label': c, 'value': c}
                                          for c in df.select_dtypes(include='float64').columns]
                                 ),
                    width={'size': 4, 'offset': 2, 'order': 2}
                )
            )),
            html.Div(id='container2', children=[])

        ])
    div_children = new_child
    return new_child


@app.callback(Output('Region-Dropdown', 'options'),
              [Input('filter-Dropdown', 'value')],
              )
def updateDbcRegion(First_filter):
    return [{'label': c, 'value': c}
            for c in df[First_filter].fillna('Autres').unique()]


@app.callback(Output('container2', 'children'),
              [Input('categorie-Dropdown', 'value'),
               Input('Region-Dropdown', 'value'),
               Input('filter-Dropdown', 'value'),
               Input('Stastitic-Dropdown', 'value')],
              [State('container2', 'children')]
              )
def update_graphics(categorie, region, first_filter, stats,children):
    data = df[df[first_filter] == region]
    valeur = [data[categorie].size,
              data[categorie].min(axis=0),
              data[categorie].max(axis=0),
              round(data[categorie].mean(axis=0), 4),
              round(data[categorie].std(axis=0), 4),
              round(data[categorie].skew(axis=0), 4),
              round(data[categorie].kurtosis(axis=0), 4)]
    files = pd.DataFrame(data={'Statistiques': Statistiques, 'Valeur': valeur})
    # create some matplotlib graph
    nom = 'image'
    dta = data[categorie]
    data2 = data.groupby('Date')[categorie].agg([np.mean, min, max, np.std, np.sum, np.median])
    df2 = df.groupby('Date')[categorie].agg([np.mean, min, max, np.std, np.sum, np.median])
    datahist = dta.dropna()
    a, b, err = estimation_loi_weibull(datahist)
    paramsWeibull = pd.DataFrame(data={'a': a, 'b': b, 'MSE': err}, index=[0])

    xhist, cdf = plotWeibParams(datahist, a, b)
    Librairie_2021.histo_Continue(datahist, 10, nom)
    aujourdhui = datetime.datetime.today()
    jour = "{}{}{}".format(aujourdhui.timetuple()[2], aujourdhui.timetuple()[1], aujourdhui.timetuple()[0])
    nom_fig = "{}_histo_{}.png".format(nom, jour)
    test_base64 = base64.b64encode(open(nom_fig, 'rb').read()).decode('ascii')
    div_children2 = html.Div(
        children=[
            html.Br(),
            dbc.Col(
                html.Hr(),
                width={'size': 10, 'offset': 1, 'order': 1}
            ),
            html.H3('Analyse statistique de ' + categorie + " pour " + region
                    , style={"textAlign": "center"}),
            html.Br(),
            html.Br(),
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
                            'textAlign': 'left',
                            'fontWeight': 'bold'
                        } for c in ['country', 'iso_alpha3']
                    ],
                    style_data={  # overflow cells' content into multiple lines
                        'whiteSpace': 'normal',
                        'height': '50px',
                        'lineHeight': '15px',
                        'fontWeight': 'bold'
                    }),
                    width={'size': 4, "offset": 1, 'order': 1}
                ),
                dbc.Col(html.Img(id='Image',
                                 src='data:image/png;base64,{}'.format(test_base64),
                                 style={'height': '95%', 'width': '110%'},
                                 # style={'width': '40vh', 'height': '60vh'},

                                 ),

                        width={'size': 4, "offset": 1, 'order': 2}
                        )
            ]),
            html.Br(),
            dbc.Col(
                html.Hr(),
                width={'size': 10, 'offset': 1, 'order': 1}
            ),
            html.Br(),
            html.H3('Evolution du ' + categorie + " pour " + region + " en fonction du temps"
                    , style={"textAlign": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col(dcc.Graph(id="scatter_chart",
                                  figure={
                                      'data': [
                                          go.Scatter(
                                              x=data2.index,
                                              y=data2[stats],
                                              mode='lines',
                                              name=region,
                                              marker_color='rgb(55, 83, 109)'
                                          ),
                                          go.Scatter(
                                              x=df2.index,
                                              y=df2[stats],
                                              mode='lines',
                                              name=" pour tous les " + first_filter,
                                              marker_color='rgb(26, 118, 255)',
                                              opacity=0.3
                                          )

                                      ],
                                      'layout': go.Layout(
                                          title={
                                              'text': categorie + " <br> (en " + stats + ") <br> " + region +
                                                      " vs  pour tous les " + first_filter,
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
                        width={'size': 5, "offset": 1, 'order': 2}
                        ),
                dbc.Col(dcc.Graph('scatter_chart2',
                                  figure={
                                      'data': [go.Scatter(
                                          x=data2.index,
                                          y=data2[stats],
                                          mode='lines',
                                          name=region,
                                      )
                                      ],
                                      'layout': go.Layout(
                                          title={
                                              'text': categorie + " <br> (en " + stats + ")  pour " + region,
                                              # 'text': categorie + " <br> (en " + stats + ")  pour tous les " + first_filter,
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
                                          },
                                          # margin={
                                          #  'l': 10, 'b': 20, 't': 0, 'r': 0
                                          # },
                                      )
                                  }
                                  ),
                        width={'size': 5, "offset": 1, 'order': 1}
                        )

            ]),
            html.Br(),
            dbc.Col(
                html.Hr(),
                width={'size': 10, 'offset': 1, 'order': 1}
            ),
            html.Br(),
            html.H2('Estimation de la loi suivi Par : ' + categorie, style={"textAlign": "center"}),
            html.Br(),
            dcc.Markdown('''
            On fait l'hypothèse que ''' + categorie + " pour " + region + ''' suit une loi de Weibull
             dont la fonction de repartition s'écrit F(x,a,b) = 1 - exp(-(x/b)^a),
             
            On estime les paramètres a et b de loi en utilisant la méthode du rang médian 
            ''',
                         style={"textAlign": "center",
                                "font-size": "18px"}
                         ),
            dbc.Col(dash_table.DataTable(
                id='EstimationWeibull_table',
                columns=[{"name": i, "id": i} for i in ["a", "b", "MSE"]],
                data=paramsWeibull.to_dict('records'),
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
            dbc.Row(
                id='estimation-loi',
                children=[
                    dbc.Col(
                        dcc.Graph(
                            id='histo-line',
                            style={'height': '80vh'},
                            figure={
                                'data': [
                                    go.Histogram(
                                        x=datahist,
                                        #nbinsx=15,
                                        xbins=dict(
                                            start=min(datahist),
                                            end=max(datahist),
                                            size=(max(datahist)-min(datahist))/10
                                        ),
                                        name="donnée historique",
                                        histnorm='probability density',
                                        marker_color='rgb(55, 83, 109)',
                                        marker_line_width=1,
                                        marker_line_color="white",
                                        opacity=0.75),
                                    go.Scatter(x=xhist,
                                               y=cdf,
                                               mode='lines',
                                               name='loi de Weibull estimé',
                                               marker_color='rgb(26, 118, 255)')
                                ],
                                'layout': go.Layout(
                                    title='Comparaison des densité de probabilités',
                                    xaxis_tickfont_size=14,
                                    yaxis=dict(
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    ),
                                    xaxis=dict(
                                        title=categorie,
                                        titlefont_size=16,
                                        tickfont_size=14,
                                    ),
                                    legend=dict(
                                        x=1.0,
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
        ]
    )
    #children.append(div_children2)
    return div_children2
