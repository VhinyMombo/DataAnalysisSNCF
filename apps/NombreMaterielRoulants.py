#### importation des modules ###############

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import app
from function import build_hierarchical_dataframe

################################################################
df = pd.read_csv(
    "https://ressources.data.sncf.com/explore/dataset/nombre-de-materiels-roulants-sncf-voyageurs-exploitables-par-serie-activite/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
    sep=';')
##################################################################
layout = html.Div([
    dcc.Markdown(
        '''
        Ce jeu de données affiche le nombre de matériels roulants SNCF Voyageurs exploitables par série et par activité.

Situation du Matériel = Exploitable

Libellé ECM (En Charge de la Maintenance) = SNCF Mobilité

Libellé Détenteur = SNCF Mobilité

Libellé Exploitant = TER, Intercités, Transilien, Voyages SNCF

Les matériels roulants des filiales (Thalys, etc.) sont hors périmètre.

Pour le cas de la série V2N, chaque caisse correspond à un matériel roulant.
        ''',
        style={"textAlign": "center",
               "font-size": "18px"}
    ),
    html.H4('Materiel en circulation', style={"textAlign": "center"}),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='PIE-Dropdown1',
                         multi=False,
                         value=df.select_dtypes(include='object').columns[0],
                         placeholder='Select a filter',
                         options=[{'label': c, 'value': c}
                                  for c in df.select_dtypes(include='object').columns]
                         ),
            width={'size': 4, 'offset': 1, 'order': 1}
        ),
        dbc.Col(
            id="Pie-Col",
            children=[],
            width={'size': 4, 'offset': 2, 'order': 1}
        ),

    ]),
    html.Div(id='PieChart-div', children=[]),
    # dcc.Graph(id='PieChart'),
],
    style={'marginBottom': 50, 'marginTop': 25}

)


###################################################
@app.callback(
    Output('Pie-Col', 'children'),
    [Input('PIE-Dropdown1', 'value')],
    [State('Pie-Col', 'children')]
)
def update_dropdown2(dropValue,dcc_children):
    dff = df.select_dtypes(include='object').columns
    dff = dff.drop(dropValue)
    dcc_children = dcc.Dropdown(id='PIE-Dropdown2',
              multi=False,
              value=dff[0],
              placeholder='Select a filter',
              options=[{'label': c, 'value': c}
                       for c in dff]
              )
    return dcc_children

@app.callback(
    Output('PieChart-div', 'children'),
    [Input('PIE-Dropdown1', 'value'),
     Input('PIE-Dropdown2', 'value')],
    [State('PieChart-div', 'children')]
)
def updatePIechart(materiel1, materiel2, div_children5):
    dff = df.groupby(materiel1).agg("sum")
    levels = [materiel2, materiel1]  # levels used for the hierarchical chart
    color_columns = ['Nombre de matériels exploitables', 'Nombre de matériels exploitables']
    value_column = 'Nombre de matériels exploitables'
    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)

    div_children5 = html.Div(
        children=[
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="PieChart",
                        style={'width': '80vh', 'height': '80vh'},
                        figure={
                            'data': [
                                go.Pie(values=dff["Nombre de matériels exploitables"],
                                       labels=dff.index,
                                       textinfo='label+percent',
                                       name=materiel1,
                                       title=df.select_dtypes(include='int64').columns[0],
                                       ),
                            ],
                            'layout': go.Layout(
                                xaxis_tickfont_size=14,
                                margin=dict(t=10, b=10, r=10, l=10),
                                legend=dict(
                                    x=1.0,
                                    y=1.0,
                                    bgcolor='rgba(255, 255, 255, 0)',
                                    bordercolor='rgba(255, 255, 255, 0)'
                                )


                            )
                        }
                    ),
                    width={'size': 5, 'offset': 1, 'order': 1}

                ),
                dbc.Col(
                    dcc.Graph(
                        id='Sunburst',
                        style={'width': '80vh', 'height': '80vh'},
                        figure={
                            'data': [
                                go.Sunburst(
                                    labels=df_all_trees['id'],
                                    parents=df_all_trees['parent'],
                                    values=df_all_trees['value'],
                                    branchvalues='total',
                                    marker=dict(
                                        colorscale='RdBu',
                                        cmid=0.5310344827586206),
                                    hovertemplate='<b>%{label} </b> <br> Nombre de matériel <br> exploitable: %{value}',
                                    name=''
                                )
                            ],
                            'layout': go.Layout(
                                margin=dict(t=10, b=10, r=10, l=10)
                            )
                        }
                    ),
                    width={'size': 5, 'offset':1, 'order': 2}
                )
            ])
        ],
        style={'marginBottom': 50, 'marginTop': 25}
    )
    return div_children5


''''
    fig = px.pie(data_frame= dff,
                 values=dff.select_dtypes(include='int64').columns[0],
                 names=materiel,
                 title=dff.select_dtypes(include='int64').columns[0])
    fig.show()
    return fig'''
