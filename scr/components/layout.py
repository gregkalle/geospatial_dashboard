from dash import Dash, html
from .data_dropdown import render as data_dropdown
import components.ids as ids


def create_layout(app:Dash)->html.Div:
    return html.Div(className=ids.LAYOUT,
                    children=[
                        html.H1(id=ids.HEADER1_NAME,children="Dashboard to show geospatial data"),
                        html.Hr(),
                        html.Div(className=ids.DROPDOWN_CONTAINER,
                                 children=[data_dropdown(app)])
                    ]
    )
