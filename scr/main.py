from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout
from components.app_variables import Values

def main()->None:

    #load data
    values = Values()
    #intitalize the app
    app = Dash(external_stylesheets=[BOOTSTRAP])
    #set title
    app.title = "Geospatial Dashboard"
    #create layout
    app.layout = create_layout(app,values)
    #run the app
    app.run(debug=True)


if __name__ == "__main__":
    main()
