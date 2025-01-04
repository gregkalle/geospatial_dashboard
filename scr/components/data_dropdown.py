from dash import Dash, html, dcc, Input, Output
import components.ids as ids
from assets.style import COLOR

def render(app:Dash)->html.Div:

    #data to use in the dropdown
    #TODO: Data have to be changed to the actual data
    all_data = ["country1","country2","country3"]

    @app.callback(Output(ids.DATA_DROPDOWN,"value"),Input(ids.SELECT_ALL_BUTTON,"n_clicks"))
    def select_all_countries(n_clicks:int)->list[str]:
        return all_data

    return html.Div(
        children=[
            html.H6("Select a country"),
            dcc.Dropdown(
                style={"background-color":COLOR['background'],"color":COLOR['text']},
                id=ids.DATA_DROPDOWN,
                options=[{"label":data,"value":data} for data in all_data],
                value=all_data,
                multi=True                
            ),
            html.Button(
                className=ids.DROPDOWN_BUTTON,
                id=ids.SELECT_ALL_BUTTON,
                children=["Select all countries"]
            )
        ]
    )