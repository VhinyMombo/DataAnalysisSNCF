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
from apps import regularite, tempTravail, NombreMaterielRoulants

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

container = dbc.Container([
    header,
    content,
])


# Menu callback, set and return
# Declare function.py  that connects other pages with content to container
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([dcc.Markdown('''
            ### The Application
            This application was built by [Vhiny-Guilley](https://linkedin.com/in/vhinyguilley-mombo) at departement de 
            de mathematique CNAM supervised by [Dariush Ghorbanzadeh](https://maths.cnam.fr/Membres/ghorbanzadeh/)
            Using historical SNCF data,
            this application provides visualizations for regularity statistics dating from 1991 to 2020. Selecting
            from a dropdown menu, the era will update the list of available teams and players in the range set on the years
            slider. The slider allows the user to adjust the range of years with which the data is presented.
            ### The Analysis
            We are still working on it!! we are back soon !!
            ### The Data
            The data used in this application was retrieved from [SNCF Data ressources](https://ressources.data.sncf.com/pages/accueil/).
            This database is copyright 1996-2021 by SNCF. This data is licensed under a Creative Commons Attribution-ShareAlike
            3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
        ''')], className='home')
    elif pathname == '/apps/regularite':
        return regularite.layout
    elif pathname == '/apps/tempTravail':
        return tempTravail.layout
    elif pathname == '/apps/NombreMaterielRoulants':
        return NombreMaterielRoulants.layout
    else:
        return 'ERROR 404: Page not found!'


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
