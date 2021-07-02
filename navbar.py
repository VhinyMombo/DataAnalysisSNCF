# Import Bootstrap from Dash
import dash_bootstrap_components as dbc


# Navigation Bar function
def Navbar():
    navbar = dbc.NavbarSimple(children=[
        dbc.NavItem(dbc.NavLink("Analyse de la regularité mensuelle", href='/apps/regularite')),
        dbc.NavItem(dbc.NavLink("Temps de Travail", href='/apps/tempTravail')),
        dbc.NavItem(dbc.NavLink("Nombre de matériels roulants", href='/apps/NombreMaterielRoulants')),
    ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color="light",
        dark=False,
        expand='lg', )
    return navbar
