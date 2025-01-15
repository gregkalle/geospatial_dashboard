from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
from plotly import colors
import components.ids as ids
from components.app_variables import Values

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
        )

    @app.callback(Output(ids.FOOTPRINT_HISTO_GRAPH, "figure"),
                  [Input(ids.RANGE_SLIDER, "value"),
                   Input(ids.SUPLOTS_GRAPH, "clickData")])
    def update_graph(years:int, clickdata_suplots:dict)->dict:

        
        data_frame = values.df.dropna(subset=["co2_per_capita","iso_code","year"])
        data_frame = data_frame[data_frame["iso_code"].isin(values.country_iso_codes)]
        data_frame = data_frame[["year","co2_per_capita","iso_code"]]
        data_frame = data_frame[data_frame["year"].isin([years[0]+i for i in range(years[1]-years[0]+1)])]

        color_schema = colors.qualitative.Dark24[values.subplot_color_offset:] + colors.qualitative.Dark24[:values.subplot_color_offset]

        if ctx.triggered_id == ids.SUPLOTS_GRAPH and not values.country_iso_codes:
            return {"data":[], "layout":{}}

        new_fig = px.histogram(data_frame=data_frame,
                               x=data_frame["year"],
                               y=data_frame["co2_per_capita"],
                               nbins=years[1]-years[0]+1,
                               histfunc="sum",
                               cumulative=True,
                               color="iso_code",
                               color_discrete_sequence = color_schema
                               )
        return {"data":new_fig.data, "layout":new_fig.layout}


    return html.Div(className=ids.FOOTPRINT_HISTO,
                    children=[
                        dcc.Graph(id=ids.FOOTPRINT_HISTO_GRAPH,
                                  figure=fig)
                    ])