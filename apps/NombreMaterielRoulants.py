#### importation des modules ###############

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app

################################################################
df = pd.read_csv(
    "https://ressources.data.sncf.com/explore/dataset/nombre-de-materiels-roulants-sncf-voyageurs-exploitables-par-serie-activite/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
    sep=';')
##################################################################
layout = dbc.Container((
    html.H4('Materiel en circulation', style={"textAlign": "center"}),
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(id='PIE-Dropdown',
                         multi=False,
                         value=df.select_dtypes(include='object').columns[0],
                         placeholder='Select a filter',
                         options=[{'label': c, 'value': c}
                                  for c in df.select_dtypes(include='object').columns]
                         ),
            width={'size': 4, 'offset': 4, 'order': 1}
        )
    ),
    html.Div(id='PieChart-div', children=[]),
    # dcc.Graph(id='PieChart'),
),
    fluid=True
)


###################################################
@app.callback(
    Output('PieChart-div', 'children'),
    [Input('PIE-Dropdown', 'value')],
    [State('PieChart-div', 'children')]
)
def updatePIechart(materiel, div_children5):
    dff = df.groupby(materiel).agg("sum")
    div_children5 = html.Div(
        children=[
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(
                        id="PieChart",
                        style={'width': '180vh',
                               'height': '90vh',
                               "textAlign": "center"},
                        figure={
                            'data': [
                                go.Pie(values=dff["Nombre de matériels exploitables"],
                                       labels=dff.index,
                                       textinfo='label+percent',
                                       name=materiel,
                                       title=df.select_dtypes(include='int64').columns[0],
                                       ),
                            ],
                            'layout': go.Layout(
                                xaxis_tickfont_size=14,
                                legend=dict(
                                    x=0.8,
                                    y=1.0,
                                    bgcolor='rgba(255, 255, 255, 0)',
                                    bordercolor='rgba(255, 255, 255, 0)'
                                )
                            )
                        }
                    )
                )
            )
        ])
    return div_children5


''''
    fig = px.pie(data_frame= dff,
                 values=dff.select_dtypes(include='int64').columns[0],
                 names=materiel,
                 title=dff.select_dtypes(include='int64').columns[0])
    fig.show()
    return fig'''
