import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from apps import regularite
from navbar import Navbar

# Import server for deployment
from app import srv as server

# Import app
from app import app
from apps import regularite, tempTravail, NombreMaterielRoulants, EmissionCO2e

# Import server for deployment

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div([
            html.H2(children='SNCF Data Analysis'),
            html.H3(children='A Visualization of Historical Data')])
    ), className='banner')

content = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-content')
])

container = html.Div([
    header,
    content,
])


# Menu callback, set and return
# Declare function.py  that connects other pages with content to container
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            dcc.Markdown(
                '''
            ### The Application
            Cette application a été developpé par [Vhiny-Guilley](https://linkedin.com/in/vhinyguilley-mombo) durant son stage au CNAM Ile de France, sous la supervision de 
            
            [Dariush Ghorbanzadeh](https://maths.cnam.fr/Membres/ghorbanzadeh/), dans le but de faire une analyse descriptive des données de regularité, du temps de travail, etc. à la
            
            SNCF. C'est une application multipage, qui utilise plusieurs dataset, que l'on peut consulter grâce à plusieurs menu deroulant et slider pour les dates.
            
            Pour commencer, vous pouvez cliquer sur l'un des onglets ci dessus.
            
             Ceci n'est pas une versions definitive, certaines pages sont en cours de developpement.
            
            ### The Analysis
            We are still working on it!! we are back soon !!
            ### Les Données 
            
            Les données utilisées dans cette application proviennent principalement du sitr [SNCF Data ressources](https://ressources.data.sncf.com/pages/accueil/).
            Ces données sont tout droits reservées SNCF et sont sous licence Creative Commons Attribution-ShareAlike
            3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
        ''',
                style={"textAlign": "center",
                       "font-size": "18px"}

            )
        ]
        )
    elif pathname == '/apps/regularite':
        return regularite.layout
    elif pathname == '/apps/tempTravail':
        return tempTravail.layout
    elif pathname == '/apps/NombreMaterielRoulants':
        return NombreMaterielRoulants.layout
    elif pathname =='/apps/EmissionCO2e':
        return EmissionCO2e.layout


# Main index function.py that will call and return all layout variables
def index():
    layout = html.Div([
        nav,
        container
    ])
    return layout


# Set layout to index function.py
app.layout = index()

# Call app server
if __name__ == '__main__':
    # set debug to false when deploying app
    app.run_server(debug=True,port = 2000)
