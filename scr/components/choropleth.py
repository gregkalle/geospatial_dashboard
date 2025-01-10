from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from components.app_variables import Values
import components.ids as ids
from assets.style import COLOR

def get_selected_unselected_data(df:pd.DataFrame, year:int, country_names:list[str])->tuple[pd.DataFrame]:
    df_of_year = df[df["year"] == year]
    df_selected = df_of_year[df_of_year["iso_code"].isin(country_names)]
    df_unselected = df_of_year[~df_of_year["iso_code"].isin(country_names)]
    return df_selected, df_unselected


def render(app:Dash, values:Values)->html.Div:

    #drop the rows with missing values
    df = values.df.dropna(subset=["iso_code","co2_per_capita"])

    @app.callback(Output(ids.CHOROPLETH_GRAPH, "figure"),
                [Input(ids.DROPDOWN_CONTINENT, "value"),
                 Input(ids.DROPDOWN_YEAR,"value"),
                 Input(ids.CHOROPLETH_GRAPH,"clickData")
                ])
    def update_choropleth(region:str, year:int, clickData:dict)->html.Div:

        print(str(clickData))
        #set selected countries:
        if clickData is None and len(values.country_names) == 0:
            clickData = {"points":[{'location':values.DEFAULT_NATION[region]}]}
        if clickData is not None:
            values.select_country(name=clickData["points"][0]['location'])
        print(values.country_names)
        
        df_selected, df_unselected = get_selected_unselected_data(df, year, values.country_names)

        #create the choropleth map

        hovertext = "{" + "hovertext" + "}"
        z = "{" + "z" + "}"

        fig = px.choropleth(df_selected,locations="iso_code",
                            color='co2_per_capita',
                            hover_name="country",
                            range_color=(0,22),
                            labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                            color_continuous_scale=px.colors.sequential.Plasma_r,
                            )
        trace = px.choropleth(
                df_unselected,locations="iso_code",
                color='co2_per_capita',
                hover_name="country",
                range_color=(0,22),
                labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                color_continuous_scale=px.colors.sequential.Plasma_r,   
            )
        
        trace.update_traces(marker=dict(opacity=0.4))

        fig.add_trace(
            trace.data[0]
        )

        fig.update_traces(
            hovertemplate = f'<b>%{hovertext}</b><br>CO2 per capita=%{z}<extra></extra>',
            name = "World"
        )

        #update the layout
        fig.update_layout(
            title=f"CO2 per capita in {year}",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"],
            uirevision= region,
        )

        #update the font of the colorbar
        fig.update_coloraxes(
            colorbar_outlinecolor=COLOR["text"],
            colorbar_outlinewidth=0.5,
            colorbar_tickfont_color=COLOR["text"],
            colorbar_title_font_color=COLOR["text"]
        )

        #update the region
        fig.update_geos(
            scope=region,
            )


        #add datasource annotation
        fig.add_annotation(text=f"<a href=\'{values.DATA_SOURCE_URL}\' style=\'color:{COLOR['text']}\'>{values.DATA_SOURCE} {values.DATA_SOURCE_URL}</a>",
                            xanchor='right',
                            x=0.5,
                            yanchor='bottom',
                            y=-0.05,
                            showarrow=False
                        )
        
        return {"data": fig.data, "layout": fig.layout}


    return html.Div(
        children=[
            dcc.Graph(id=ids.CHOROPLETH_GRAPH,
                      style={'width': '95vw', 'height': '70vh'},
                      figure=px.choropleth())
        ],
        id=ids.CHOROPLETH
    )