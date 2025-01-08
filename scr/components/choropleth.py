from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import components.constant_values as const
import components.ids as ids
from assets.style import COLOR

COUNTRY_NAMES = set({})

def select_country(name:str)-> None:
    if name in COUNTRY_NAMES:
        COUNTRY_NAMES.remove(name)
    else:
        COUNTRY_NAMES.add(name)

def render(app:Dash, df:pd.DataFrame)->html.Div:

    @app.callback(Output(ids.CHOROPLETH, "children"),
                [Input(ids.DROPDOWN_CONTINENT, "value"),
                 Input(ids.DROPDOWN_YEAR,"value"),
                 Input(ids.CHOROPLETH_GRAPH,"clickData")
                ])
    def update_choropleth(region:str, year:int, clickData:dict)->html.Div:

        #get data from selected year
        df_of_year = df[df["year"]==year]
        
        #drop the rows with missing values
        df_of_year = df_of_year.dropna(subset=["iso_code","co2_per_capita"])

        #set selected countries:
        if clickData is None:
            clickData = {"points":[{"hovertext":"Germany"}]}
        select_country(name=clickData["points"][0]["hovertext"])

        #create the choropleth map
        fig = px.choropleth(df_of_year,locations="iso_code",
                            color='co2_per_capita',
                            hover_name="country",
                            range_color=(0,22),
                            labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                            color_continuous_scale=px.colors.sequential.Plasma_r
                            )
        #update the layout
        fig.update_layout(
            title=f"CO2 per capita in {year}",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"]
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

        #add datasource annotation
        fig.add_annotation(text=f"<a href='{const.DATA_SOURCE_URL}' style='color:{COLOR["text"]}'>{const.DATA_SOURCE} {const.DATA_SOURCE_URL}</a>",
                            showarrow=False,
                            xanchor='right',
                            x=0.5,
                            yanchor='top',
                            y=0
                        )
        #Change Annotation text color
        #fig.update_annotations(
        #    font=dict(color="#f5deb3")
        #)

        return html.Div(
            children=[
                dcc.Graph(id=ids.CHOROPLETH_GRAPH,
                          figure=fig,style={'width': '90vw', 'height': '70vh'}),
                html.Label(str(clickData)),
                html.Label(list(COUNTRY_NAMES))
            ],
            id=ids.CHOROPLETH
        )

    return html.Div(
        children=[
            dcc.Graph(id=ids.CHOROPLETH_GRAPH,
                      figure=px.choropleth())
        ],
        id=ids.CHOROPLETH
    )