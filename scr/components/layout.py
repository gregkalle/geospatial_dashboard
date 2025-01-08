from dash import Dash, html
from pandas import DataFrame
from .dropdown_continents import render as dropdown_continents
from .dropdown_year import render as dropdown_years
from .choropleth import render as choropleth
from .subplots import render as subplots
import components.ids as ids


def create_layout(app:Dash,df:DataFrame)->html.Div:
    return html.Div(className=ids.LAYOUT,
                    children=[
                        html.H1(id=ids.HEADER1_NAME,children="Dashboard to show geospatial data"),
                        html.Hr(),
                        html.Div(style={"margin-left":"20vw"},className=ids.DROPDOWN_CONTAINER,
                                 children=[dropdown_continents(app),
                                           dropdown_years(app)]),
                        html.Div(className=ids.CHOROPLETH_CONTAINER,
                                 children=[choropleth(app=app,df=df)]),
                        html.Div(
                            id=ids.SUPLOTS_CONTAINER,
                            children=[subplots(app=app,df=df)]
                        )
                    ]
    )
