from dash import Dash, html
import components.ids as ids


def create_layout(app:Dash)->html.Div:
    return html.Div(className=ids.LAYOUT,
                    children=[
                        html.H1("Dashboard to show geospatial data"),
                        html.Hr(),                        
                    ]
    )
