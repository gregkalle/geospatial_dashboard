from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import components.constant_values as const
import components.ids as ids
from assets.style import COLOR


def select_country(name:str)-> None:
    if name in const.country_names:
        const.country_names.remove(name)
    else:
        const.country_names.add(name)

def render(app:Dash, df:pd.DataFrame)->html.Div:

    @app.callback(Output(ids.CHOROPLETH, "children"),
                [Input(ids.DROPDOWN_CONTINENT, "value"),
                 Input(ids.DROPDOWN_YEAR,"value"),
                 Input(ids.CHOROPLETH_GRAPH,"clickData")
                ])
    def update_choropleth(region:str, year:int, clickData:dict)->html.Div:

        #set selected countries:
        if clickData is None and len(const.country_names) == 0:
            clickData = {"points":[{'location':const.DEFAULT_NATION[region]}]}
        if clickData is not None:
            select_country(name=clickData["points"][0]['location'])
        
        #get data from selected year
        df_of_year = df[df["year"]==year]
        
        #drop the rows with missing values
        df_of_year = df_of_year.dropna(subset=["iso_code","co2_per_capita"])

        #create selected and unselected dataframes
        df_selected = df_of_year[df_of_year["iso_code"].isin(const.country_names)]
        df_unselected = df_of_year[~df_of_year["iso_code"].isin(const.country_names)]

        #create the choropleth map
        fig = px.choropleth(df_selected,locations="iso_code",
                            color='co2_per_capita',
                            hover_name="country",
                            range_color=(0,22),
                            labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                            color_continuous_scale=px.colors.sequential.Plasma_r
                            )
        trace = px.choropleth(
                df_unselected,locations="iso_code",
                color='co2_per_capita',
                hover_name="country",
                range_color=(0,22),
                labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                color_continuous_scale=px.colors.sequential.Plasma_r                
            )
        
        trace.update_traces(marker=dict(opacity=0.7), selector=dict(type='choropleth'))

        fig.add_trace(
            trace.data[0]
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

        return html.Div(
            children=[
                dcc.Graph(id=ids.CHOROPLETH_GRAPH,
                          figure=fig,style={'width': '90vw', 'height': '70vh'}),
                html.Label(str(clickData)),
                html.Label(list(const.country_names))
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