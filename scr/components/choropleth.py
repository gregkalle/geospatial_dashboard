from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import components.ids as ids
from assets.style import COLOR

def render(app:Dash)->html.Div:
    #create dataframe
    df = pd.read_csv("scr/data/owid_co2_data.csv")

    #filter the data for the year 2023
    df_2023 = df[df["year"]==2023]
    #drop the rows with missing values
    df_2023 = df_2023.dropna(subset=["iso_code","co2_per_capita"])

    #create the choropleth map
    fig = px.choropleth(df_2023,locations="iso_code",
                        color='co2_per_capita',
                        hover_name="country",
                        range_color=(0,15),
                        labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                        color_continuous_scale=px.colors.sequential.Plasma_r)
    #update the layout
    fig.update_layout(
        title="CO2 per capita in 2023",
        title_font_color=COLOR["text"],
        title_x=0.5,
        paper_bgcolor=COLOR["background"],
        geo = dict(
            scope = "world",
        )
    )
    #update the font of the colorbar
    fig.update_coloraxes(
        colorbar_outlinecolor=COLOR["text"],
        colorbar_outlinewidth=0.5,
        colorbar_tickfont_color=COLOR["text"],
        colorbar_title_font_color=COLOR["text"]
    )
    
    return html.Div(
        dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}),
        id=ids.CHOROPLETH
    )