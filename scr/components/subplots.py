"""renders a div with a figure of three diffrent plots conected to the choropleth"""
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative
#import pycountry_convert as pc
from components.app_variables import Values
import components.ids as ids
from assets.style import COLOR

def render(app:Dash, values:Values)->html.Div:

    #drop the rows with missing values
    df = values.df.dropna(subset=["co2","co2_per_capita"])

    #add traces:
    @app.callback(Output(ids.SUPLOTS, "children"), Input(ids.CHOROPLETH_GRAPH, "clickData"))
    def update_subplots(clickData:dict)->dict:

        fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "scatter"},{"type": "histogram"}],[{"type": "scatter"},None]],
        )
    
        #update figure layout
        fig.update_layout(
            title="***placeholder***",
            title_font_color=COLOR["text"],
            title_x=0.5,
            paper_bgcolor=COLOR["background"]
        )

        

        for i,country in enumerate(values.country_names):
            scatter = fig.add_trace(go.Scatter(
                y=df[df["iso_code"]==country]["co2_per_capita"],
                x=df[df["iso_code"]==country]["year"],
                mode="lines",
                name=str(country) + "_scatter",
                line_shape = "spline"
                ),
                row=1,col=1
                )
            scatter.update_traces(
                line=dict(color=qualitative.Dark24[i%24]),
                selector={"name":str(country) + "_scatter"})
            
            histogram = fig.add_trace(go.Histogram(
                y=df[df["iso_code"]==country]["co2"],
                x=df[df["iso_code"]==country]["year"],
                nbinsx=len(df[df["iso_code"]==country]["co2"]),
                cumulative_enabled=True,
                name=str(country) + "_histogram",
                marker=dict(color=qualitative.Dark24[i%24])
                ),
                row=1,col=2)


            histogram.update_layout(
                barmode="stack"
            )

            fig.update_layout(
                uirevision=clickData,
            )
          
        return html.Div(
            children=[
                dcc.Graph(figure=fig,style={'width': '90vw', 'height': '120vh'},id=ids.SUPLOTS_GRAPH)
            ],
            id=ids.SUPLOTS
        )
     


    return html.Div(
        children=[
            dcc.Graph(style={'width': '90vw', 'height': '80vh'},id=ids.SUPLOTS_GRAPH),
        ],
        id=ids.SUPLOTS
    )