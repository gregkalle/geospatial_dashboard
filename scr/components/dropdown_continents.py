from dash import Dash, html, dcc
import components.ids as ids
from assets.style import COLOR

def render(app:Dash)->html.Div:

    #TODO megrate the dataframe in main and add to render-funktions

    #data to use in the dropdown
    all_continents = ['world','africa', 'asia', 'europe', 'north america', 'south america']

    return html.Div(
        children=[
            html.H6("Select a region to display on the map:"),
            dcc.Dropdown(
                style={"background-color":COLOR['background'],"color":COLOR['text']},
                id=ids.DROPDOWN_CONTINENT,
                options=[{"label":continent.upper(),"value":continent} for continent in all_continents],
                value=all_continents[0],
                clearable=False            
            )
        ]
    )