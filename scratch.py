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
