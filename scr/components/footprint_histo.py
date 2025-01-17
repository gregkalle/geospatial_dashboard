from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.express as px
from plotly import colors
import components.ids as ids
from components.app_variables import Values
from assets.style import COLOR

def render(app:Dash, values:Values)->html.Div:

    years = [values.YEAR_START, values.YEAR_MAX]

    data_frame = values.df.dropna(subset=["co2_per_capita","iso_code","year"])
    data_frame = data_frame[data_frame["iso_code"].isin(values.country_iso_codes)]
    data_frame = data_frame[["year","co2_per_capita","iso_code"]]
    data_frame = data_frame[data_frame["year"].isin([years[0]+i for i in range(years[1]-years[0]+1)])]

    color_schema = colors.qualitative.Dark24[values.subplot_color_offset:] + colors.qualitative.Dark24[:values.subplot_color_offset]

    fig = px.histogram(
        data_frame=data_frame,
        x=data_frame["year"],
        y=data_frame["co2_per_capita"],
        nbins=int(years[1] - years[0] + 1),
        histfunc="sum",
        cumulative=True,
        color="iso_code",
        color_discrete_sequence=color_schema,
        labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
        )
    
    fig.update_layout(
            title=f"Co2 emission per capita cumulative from {years[0]} to {years[1]}",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"],
            font_color=COLOR["text"],
        )

    @app.callback(Output(ids.FOOTPRINT_HISTO_GRAPH, "figure"),
                  [Input(ids.RANGE_SLIDER, "value"),
                   Input(ids.SUPLOTS_GRAPH, "clickData")],
                   State(ids.FOOTPRINT_HISTO_GRAPH, "figure"))
    def update_graph(years:int, clickdata_suplots:dict, figure_before:dict)->dict:

        
        data_frame = values.df.dropna(subset=["co2_per_capita","iso_code","year"])
        data_frame = data_frame[data_frame["iso_code"].isin(values.country_iso_codes)]
        data_frame = data_frame[["year","co2_per_capita","iso_code"]]
        data_frame = data_frame[data_frame["year"].isin([years[0]+i for i in range(years[1]-years[0]+1)])]

        color_schema = colors.qualitative.Dark24[values.subplot_color_offset:] + colors.qualitative.Dark24[:values.subplot_color_offset]

        if (ctx.triggered_id == ids.SUPLOTS_GRAPH and not values.country_iso_codes)\
            or (ctx.triggered_id == ids.RANGE_SLIDER and not figure_before["data"]):

            figure_before["layout"]["title"]["text"] = f"Co2 emission per capita cumulative from {years[0]} to {years[1]}"

            return {"data":[], "layout":figure_before["layout"]}

        new_fig = px.histogram(data_frame=data_frame,
                               x=data_frame["year"],
                               y=data_frame["co2_per_capita"],
                               nbins=years[1]-years[0]+1,
                               histfunc="sum",
                               cumulative=True,
                               color="iso_code",
                               color_discrete_sequence = color_schema,
                               labels={"co2_per_capita":"CO2 per capita", "iso_code":"Country Code"},
                               )
        #update figure layout
        new_fig.update_layout(
            title=f"Co2 emission per capita cumulative from {years[0]} to {years[1]}",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"],
            font_color=COLOR["text"],
        )

        return {"data":new_fig.data, "layout":new_fig.layout}


    return html.Div(className=ids.FOOTPRINT_HISTO,
                    children=[
                        dcc.Graph(id=ids.FOOTPRINT_HISTO_GRAPH,
                                  figure=fig)
                    ])