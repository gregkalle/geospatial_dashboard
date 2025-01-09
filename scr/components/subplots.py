"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from dash import Dash, html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pycountry_convert as pc
import pandas as pd
import components.constant_values as const
import components.ids as ids
from assets.style import COLOR

def render(app:Dash, df:pd.DataFrame):

    #drop the rows with missing values
    df = df.dropna(subset=["co2","co2_per_capita"])

    #tmp variable to store the selected countries
    const.country_names = set(["DEU"])

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
    for country in const.country_names:
        fig.add_trace(go.Scatter(
            x=df[df["iso_code"]==country]["year"],
            y=df[df["iso_code"]==country]["co2_per_capita"],
            name=country),
            row=1,col=1
            )

    for country in const.country_names:
        fig.add_trace(go.Histogram(
            x=df[df["iso_code"]==country]["co2"],
            cumulative_enabled=True,
            name=country),
            row=1,col=2)

    
    """
    #pc country_code
    CONTINENT = {"EU":[],"AS":[],"AF":[],"NA":[],"SA":[],"OC":[]}

        
        for country in df_selected["iso_code"].to_list() +  df_unselected["iso_code"].to_list():  
           
            try:
                alpha2 = pc.country_alpha3_to_country_alpha2(country)
                conti_code = pc.country_alpha2_to_continent_code(alpha2)
                print(pc.country_alpha2_to_country_name(alpha2))
            except KeyError:
                continue
            CONTINENT[str(conti_code)].append(pc.country_alpha2_to_country_name(alpha2))
        with open("countries","a") as file:
            file.write(str(CONTINENT)+"\n")       
    
    """

    return html.Div(
        children=[
            dcc.Graph(figure=fig,style={'width': '90vw', 'height': '120vh'})
        ],
        id=ids.SUPLOTS
    )