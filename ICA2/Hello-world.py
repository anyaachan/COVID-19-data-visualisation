from dash import Dash, dcc 
import dash_bootstrap_components as dbc #CSS/JS framework that contains design templates. Will help to style your app and to customize layout.

#Firts part is components. Building the components: 
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP]) #Starting the app and choosing a theme for our app
myText = dcc.Markdown(children = "# Hello World ") #Markdown is a text 

#Customise the layout of the app
app.layout = dbc.Container([myText])

if __name__ == "__main__":
    app.run_server()

