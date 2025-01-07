from dash import Dash, html, dcc
import components.ids as ids
from assets.style import COLOR

def render(app:Dash)->html.Div:

    #data to use in the dropdown
    #TODO: Data have to be changed to the actual data
    all_data = ['world','africa', 'asia', 'europe', 'north america', 'south america']

    return html.Div(
        children=[
            html.H6("Select a region to display on the map:"),
            dcc.Dropdown(
                style={"background-color":COLOR['background'],"color":COLOR['text']},
                id=ids.DATA_DROPDOWN,
                options=[{"label":data.upper(),"value":data} for data in all_data],
                value=all_data[0]            
            )
        ]
    )