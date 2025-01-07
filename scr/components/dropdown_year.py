from dash import Dash, html, dcc
import components.ids as ids
from components.constant_values import START_YEAR
from assets.style import COLOR


def render(app:Dash)->html.Div:

    #TODO megrate the dataframe in main and add to render-funktions
    max_year = 2023
    
    selectable_years = [max_year - i for i in range(max_year-START_YEAR)]

    return html.Div(
        children=[
            html.H6("Select the year which the data belong to."),
            dcc.Dropdown(
                style={"background-color":COLOR['background'],"color":COLOR['text']},
                id=ids.DROPDOWN_YEAR,
                options=[{"label":str(year),"value":year} for year in selectable_years],
                value=selectable_years[0],
                clearable=False
            )
        ]
    )
