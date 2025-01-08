from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
from components.layout import create_layout
import components.constant_values as const

def main()->None:
    #load data
    df = pd.read_csv(const.DATA_URL)

    #intitalize the app
    app = Dash(external_stylesheets=[BOOTSTRAP])
    #set title
    app.title = "Geospatial Dashboard"
    #create layout
    app.layout = create_layout(app,df)
    #run the app
    app.run(debug=True)


if __name__ == "__main__":
    main()
