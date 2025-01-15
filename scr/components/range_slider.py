from dash import Dash, html, dcc, Input, Output, State, ctx
import components.ids as ids
from components.app_variables import Values

def render(app:Dash, values:Values)->html.Div:
    return html.Div(
        className=ids.RANGE_SLIDER_DIV,
        children=[
            html.H6("Select the start and end year of the footprint:"),
            dcc.RangeSlider(
                id=ids.RANGE_SLIDER,
                min=values.YEAR_START,
                max=values.YEAR_MAX,
                step=1,
                marks=None,
                value=[values.YEAR_START,values.YEAR_MAX],
                tooltip={"always_visible":True, "placement":"bottom"},
                updatemode="mouseup"
            )
        ]
    )