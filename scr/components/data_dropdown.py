from dash import Dash, html, dcc, Input, Output
import components.ids as ids
from assets.style import COLOR

def render(app:Dash)->html.Div:

    #data to use in the dropdown
    #TODO: Data have to be changed to the actual data
    all_data = ["country1","country2","country3"]

    return html.Div(
        children=[
            html.H6("Select a country"),
            dcc.Dropdown(
                style={"background-color":COLOR['background'],"color":COLOR['text']},
                id=ids.DATA_DROPDOWN,
                options=[{"label":data,"value":data} for data in all_data],
                value=all_data,
                multi=True                
            )
        ]
    )