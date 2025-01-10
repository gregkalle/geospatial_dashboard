from dash import Dash, html, dcc
import components.ids as ids
from components.app_variables import Values
from assets.style import DROPDOWN_STYLE


def render(app:Dash, values:Values)->html.Span:

    #TODO megrate the dataframe in main and add to render-funktions
    max_year = 2023
    
    selectable_years = [max_year - i for i in range(max_year-values.START_YEAR+1)]

    return html.Span(className=ids.DROPDOWN_SPAN,
        children=[
            html.H6("Select the year which the data belong to."),
            dcc.Dropdown(
                style=DROPDOWN_STYLE,
                id=ids.DROPDOWN_YEAR,
                options=[{"label":str(year),"value":year} for year in selectable_years],
                value=selectable_years[0],
                clearable=False
            )
        ]
    )
