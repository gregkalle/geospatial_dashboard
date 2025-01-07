from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import components.ids as ids
from assets.style import COLOR



def render(app:Dash)->html.Div:

    #TODO megrate the dataframe in main and add to render-funktions

    #create dataframe
    df = pd.read_csv("https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv")

    @app.callback(Output(ids.CHOROPLETH, "children"),
                [Input(ids.DROPDOWN_CONTINENT, "value"),
                 Input(ids.DROPDOWN_YEAR,"value")
                ])
    def update_choropleth(region:str, year:int)->html.Div:

        #get data from selected year
        df_of_year = df[df["year"]==year]
        
        #drop the rows with missing values
        df_of_year = df_of_year.dropna(subset=["iso_code","co2_per_capita"])

        #create the choropleth map
        fig = px.choropleth(df_of_year,locations="iso_code",
                            color='co2_per_capita',
                            hover_name="country",
                            range_color=(0,22),
                            labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                            color_continuous_scale=px.colors.sequential.Plasma_r)
        #update the layout
        fig.update_layout(
            title=f"CO2 per capita in {year}",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"],
        )
        #update the font of the colorbar
        fig.update_coloraxes(
            colorbar_outlinecolor=COLOR["text"],
            colorbar_outlinewidth=0.5,
            colorbar_tickfont_color=COLOR["text"],
            colorbar_title_font_color=COLOR["text"]
        )

        #update the region
        fig.update_geos(scope=region)
        return html.Div(
            dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}),
            id=ids.CHOROPLETH
        )

    return html.Div(
        id=ids.CHOROPLETH
    )