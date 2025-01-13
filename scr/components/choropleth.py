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

def render_trace(df:pd.DataFrame, trace_name:str, opacity:float = 1)->px.choropleth:
    trace = px.choropleth(df,locations="iso_code",
                            color='co2_per_capita',
                            hover_name="country",
                            range_color=(0,22),
                            labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                            color_continuous_scale=px.colors.sequential.Plasma_r,
                            )
    trace.update_traces(marker=dict(opacity=opacity),
                        name = trace_name)
    return trace

def render_layout(year:int, values:Values)->dict:
    return {"title" : f"CO2 per capita in {year}",
            "title_font_color" : COLOR["text"],
            "title_x":0.5,
            "paper_bgcolor":COLOR["background"],
            "margin":{"b":20}}

def render_trace_update()->dict:
    hovertext = "{" + "hovertext" + "}"
    z = "{" + "z" + "}"
    return {"hovertemplate" : f'<b>%{hovertext}</b><br>CO2 per capita=%{z}<extra></extra>'}

def render_colorbar_update()->dict:
    return {"colorbar":{"outlinecolor":COLOR["text"],
                        "outlinewidth":0.5,
                        "tickfont":{"color":COLOR["text"]},
                        "title":{"font":{"color":COLOR["text"]}}}}

def render_geo_update(region:str)->dict:
    return {"scope":region}

def render_annotation(values:Values)->dict:
    return {"text":f"<a href=\'{values.DATA_SOURCE_URL}\' style=\'color:{COLOR['text']}\'>{values.DATA_SOURCE} {values.DATA_SOURCE_URL}</a>",
            "xanchor":"right",
            "x":0.5,
            "yanchor":"bottom",
            "y":-0.05,
            "showarrow":False,
            "font":{"color":COLOR["text"]}}


def render(app:Dash, values:Values)->html.Div:

    #drop the rows with missing values
    df = values.df.dropna(subset=["iso_code","co2_per_capita"])

    #make selected and unselected df
    df_selected, df_unselected = get_selected_unselected_data(df, values.year, values.country_names)
    
    #create the choropleth map
    fig = render_trace(df=df_selected, trace_name=ids.SELECTED_COUNTRIES)
    fig.add_trace(
        render_trace(df=df_unselected,trace_name=ids.UNSELECTED_COUNTRIES, opacity=0.4).data[0]
        )
    #update the trace
    fig.update_traces(render_trace_update())

    #update the layout
    fig.update_layout(
        render_layout(values.year, values)
    )

    #update the font of the colorbar
    fig.update_coloraxes(render_colorbar_update())

    #update the region
    fig.update_geos(
        render_geo_update(values.region)
        )


    #add datasource annotation
    fig.add_annotation(render_annotation(values))


    @app.callback(Output(ids.CHOROPLETH_GRAPH, "figure"),
                [Input(ids.DROPDOWN_CONTINENT, "value"),
                 Input(ids.DROPDOWN_YEAR,"value"),
                 Input(ids.CHOROPLETH_GRAPH,"clickData")
                ])
    def update_choropleth(region:str, year:int, clickData:dict)->dict:

        #set selected countries:
        if (not region == values.region) and (len(values.country_names)) > 0:
            pass
        elif (not region == values.region) and (len(values.country_names) == 0):
            clickData = {"points":[{'location':values.DEFAULT_NATION[region]}]}
            values.select_country(name=clickData["points"][0]['location'])
        elif not year == values.year and len(values.country_names) > 0:
            pass
        else:
            if clickData is None and len(values.country_names) == 0:
                clickData = {"points":[{'location':values.DEFAULT_NATION[region]}]}
            if clickData is not None:
                values.select_country(name=clickData["points"][0]['location'])

        df_selected, df_unselected = get_selected_unselected_data(df, year, values.country_names)

        #create the choropleth map

        fig.update_traces(
            locations=df_selected["iso_code"],
            z=df_selected["co2_per_capita"],
            customdata=df_selected["country"],
            selector={"name":ids.SELECTED_COUNTRIES}
        )
        fig.update_traces(
            locations=df_unselected["iso_code"],
            z=df_unselected["co2_per_capita"],
            customdata=df_unselected["country"],
            selector={"name":ids.UNSELECTED_COUNTRIES}
            )
        
        fig.update_geos(
            scope=region
        )

        fig.update_layout(
            uirevision = region
        )

        values.region = region
        values.year = year

        return {"data": fig.data, "layout": fig.layout}
        

    return html.Div(
        children=[
            dcc.Graph(id=ids.CHOROPLETH_GRAPH,
                      style={'width': '95vw', 'height': '60vh'},
                      figure=px.choropleth())
        ],
        id=ids.CHOROPLETH
    )