from dash import Dash, html
from .dropdown_continents import render as dropdown_continents
from .dropdown_year import render as dropdown_years
from .choropleth import render as choropleth
from .subplots import render as subplots
from .range_slider import render as range_slider
import components.ids as ids
from components.app_variables import Values


def create_layout(app:Dash,values:Values)->html.Div:
    return html.Div(className=ids.LAYOUT,
                    children=[
                        html.H1(id=ids.HEADER1_NAME,children="Dashboard to show geospatial data"),
                        html.Hr(),
                        html.Div(style={"margin-left":"20vw"},className=ids.DROPDOWN_CONTAINER,
                                 children=[dropdown_continents(app,values),
                                           dropdown_years(app,values)]),
                        html.Div(className=ids.CHOROPLETH_CONTAINER,
                                 children=[choropleth(app=app,values=values)]),
                        html.Div(
                            id=ids.SUPLOTS_CONTAINER,
                            children=[subplots(app=app,values=values)]
                        ),
                        html.Div(className=ids.RANGE_SLIDER_CONTAIENER,
                                 children=[range_slider(app=app,values=values)])

                    ]
    )
