# Import Bootstrap from Dash
import dash_bootstrap_components as dbc


# Navigation Bar function
def Navbar():
    navbar = dbc.NavbarSimple(children=[
        dbc.NavItem(dbc.NavLink("Analyse de la regularité mensuelle", href='/apps/regularite')),
        dbc.NavItem(dbc.NavLink("Temps de Travail", href='/apps/tempTravail')),
        dbc.NavItem(dbc.NavLink("Nombre de matériels roulants", href='/apps/NombreMaterielRoulants')),
        dbc.NavItem(dbc.NavLink("Émissions de CO2e sur les liaisons TGV", href='/apps/EmissionCO2e')),

    ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color="light",
        dark=False,
        expand='lg', )
    return navbar
