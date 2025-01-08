"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from dash import Dash, html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pycountry_convert as pc
import pandas as pd
import components.ids as ids
from assets.style import COLOR

def render(app:Dash, df:pd.DataFrame):

    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.33, 0.33, 0.33],
        specs=[[{"type": "scatter"},{"type": "scatter"},{"type": "scatter"}]]
        )
    
    fig.update_layout(
            title="***placeholder***",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"]
        )
    
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
            dcc.Graph(figure=fig, style=COLOR)
        ],
        id=ids.SUPLOTS
    )