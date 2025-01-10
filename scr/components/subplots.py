"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from dash import Dash, html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import pycountry_convert as pc
from components.app_variables import Values
import components.ids as ids
from assets.style import COLOR

def render(app:Dash, values:Values)->html.Div:

    #drop the rows with missing values
    df = values.df.dropna(subset=["co2","co2_per_capita"])

    #make figure with 3 subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "scatter"},{"type": "histogram"}],[{"type": "scatter"},None]],
        )
    
    #update figure layout
    fig.update_layout(
            title="***placeholder***",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"]
        )
    #add traces:
    for country in values.country_names:
        fig.add_trace(go.Scatter(
            x=df[df["iso_code"].isin(values.country_names)]["year"],
            y=df[df["iso_code"]==country]["co2_per_capita"],
            name=country,
            ),
            row=1,col=1
            )

    for country in values.country_names:
        fig.add_trace(go.Histogram(
            x=df[df["iso_code"]==country]["co2"],
            nbinsx=len(df[df["iso_code"]==country]["co2"]),
            cumulative_enabled=True,
            name=country),
            row=1,col=2)


    return html.Div(
        children=[
            dcc.Graph(figure=fig,style={'width': '90vw', 'height': '120vh'})
        ],
        id=ids.SUPLOTS
    )