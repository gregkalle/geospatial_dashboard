"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from dash import Dash, html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import components.ids as ids

def render(app:Dash, df:pd.DataFrame):

    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.33, 0.33, 0.33],
        specs=[{"type": "scatter"},{"type": "scatter"},{"type": "scatter"}]
           )

    return html.Div(
        children=[
            dcc.Graph()
        ],
        id=ids.SUPLOTS
    )