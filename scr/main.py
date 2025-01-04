from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from components.layout import create_layout

def main():
    #intitalize the app
    app = Dash(external_stylesheets=[BOOTSTRAP])
    #set title
    app.title = "Geospatial Dashboard"
    #create layout
    app.layout = create_layout(app)
    #run the app
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
