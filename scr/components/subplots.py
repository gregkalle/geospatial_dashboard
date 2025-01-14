"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from functools import reduce
from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative
import pandas as pd
from components.app_variables import Values
import components.ids as ids
from assets.style import COLOR

def render(app:Dash, values:Values)->html.Div:
    """Renders a div with a figure of three diffrent plots conected to the choropleth.

    Args:
        app (Dash): The dash app
        values (Values): The values object

    Returns:
        html.Div: The div with the figure
    """

    #drop the rows with missing values
    df = values.df.dropna(subset=["co2","co2_per_capita"])

    #create the subplots
    @app.callback(Output(ids.SUPLOTS, "children"),
                  [Input(ids.CHOROPLETH_GRAPH, "clickData"),
                   Input(ids.SUPLOTS_GRAPH, "clickData")],
                   State(ids.SUPLOTS_GRAPH, "figure"))
    def update_subplots(clickData_choropleth:dict, clickData_suplots:dict, figure_before:dict)->dict:
        """Updates the subplots when the user clicks on a country in the choropleth or in the subplots.

        Args:
            clickData_choropleth (dict): The click data of the choropleth
            clickData_suplots (dict): The click data of the subplots
            figure_before (dict): The figure before the update

        Returns:
            dict: The updated figure
        """
        
        #create the figure
        fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "scatter"},{"type": "histogram"}]],
        subplot_titles=["CO2 emission per capita","total CO2 emission cumulative"],
        )
    
        #update figure layout
        fig.update_layout(
            title="Co2 emission progression over time",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"],
            font_color=COLOR["text"],
        )

        #update figure axes
        fig.update_xaxes(
            title="year"
        )
        fig.update_yaxes(
            title="co2 per capita in tons",
            row=1,col=1
        )
        fig.update_yaxes(
            title="co2 in million tons",
            row=1,col=2
        )
        #get the selected countries
        iso_code = [country for country in values.country_iso_codes]
        
        #if the user clicks on a country in the choropleth
        if ctx.triggered_id == ids.SUPLOTS_GRAPH and clickData_suplots["points"][0]["curveNumber"]%2 == 1:
            #get the selected country
            iso_code = [figure_before["data"][clickData_suplots["points"][0]["curveNumber"]]["name"][0:3]]
            #update the color offset
            values.SUBPLOT_COLOR_OFFSET += clickData_suplots["points"][0]["curveNumber"]//2
        
        #get the data frames for the histogram
        histo_data_frames = [df[df["iso_code"]==country][["year","co2"]].rename(columns={"co2":str(country)}) for country in iso_code]
        #merge the data frames
        histo_data = reduce(lambda left, right: pd.merge(left, right, on="year", how="outer"), histo_data_frames)
        histo_data = histo_data.fillna(0)
        
        #update the subplots
        for i,country in enumerate(iso_code):
            #add the traces to scatterplot
            scatter = fig.add_trace(go.Scatter(
                y=df[df["iso_code"]==country]["co2_per_capita"],
                x=df[df["iso_code"]==country]["year"],
                mode="lines",
                name=str(country) + " co2/capita",
                line_shape = "spline",
                ),
                row=1,col=1
                )
            #update the scatter traces
            scatter.update_traces(
                line=dict(color=qualitative.Dark24[(i+values.SUBPLOT_COLOR_OFFSET)%24]),
                selector={"name":str(country) + " co2/capita"})
            
            #add the traces to histogram
            histogram = fig.add_trace(go.Histogram(
                y=histo_data[str(country)],
                x=histo_data["year"],
                cumulative_enabled=True,
                name=str(country) + " co2",
                histfunc="sum",
                marker=dict(color=qualitative.Dark24[(i+values.SUBPLOT_COLOR_OFFSET)%24]),
                ),
                row=1,col=2)
            #update the histogram layout
            histogram.update_layout(
                barmode="stack"
            )
            #update the histogram traces
            histogram.update_traces(
                row=1,col=2,
                nbinsx=len(histo_data["year"].unique()),
            )
            #set the uirevision
            fig.update_layout(
                uirevision=clickData_choropleth,
            )

        return html.Div(
            children=[
                dcc.Graph(figure=fig,style={'width': '95vw', 'height': '55vh'},id=ids.SUPLOTS_GRAPH)
            ],
            id=ids.SUPLOTS
        )
 
    return html.Div(
        children=[
            dcc.Graph(style={'width': '95vw', 'height': '55vh'},id=ids.SUPLOTS_GRAPH),
        ],
        id=ids.SUPLOTS
    )