from dash import Dash, dcc, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc 
import plotly.express as px #Library that allows you to build graphs 

#Creating dataframe (incorporating data to the app)
df = pd.read_csv("ICA2/data-cleaned.csv")

#Building our components 
app = Dash(__name__, external_stylesheets = [dbc.themes.LUX]) #Selecting a theme and opening the app
my_title = dcc.Markdown(children = "# App that analyses COVID-19 situation") #Making the title
my_subtitle = dcc.Markdown(children= "")
my_graph = dcc.Graph(figure={}) #The figure is empty, there is nothing at the beginning 

dropdown_cases = dcc.Dropdown(options = ["cases", "deaths"],
                        value = "cases", #Setting the initial value
                        clearable = False) #Non-erasable
dropdown_year = dcc.Dropdown(options = ["2020", "2021", "2022"],
                            value = "2022",
                            clearable = False)

#Building layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([my_title], width = 6)
    ], justify="center"),
    dbc.Row([
        dbc.Col([my_subtitle], width = 6)
    ], justify="center"),
    dbc.Row([
        dbc.Col([my_graph], width = 12) 
    ], justify="center"),
    dbc.Row([
        dbc.Col([dropdown_cases], width = 6),
        dbc.Col(dropdown_year, width = 6)
    ], justify="center")
    ])

#Building a callback
#A callback decorator
@app.callback(
    Output(my_graph, component_property = "figure"),
    Output(my_subtitle, component_property = "children"),
    Input(dropdown_cases, component_property = "value"),
    Input(dropdown_year, component_property = "value")
)

#A callback function that should always go after a callback decorator 
def update_graph(cases_input, year_input):
     #график не когда я добавляю эту строчку
     
    fig = px.line(df, x = "dateRep", y = cases_input, color = "country")
    return fig, ("## " + cases_input)     #Fig goes into the output -> my_graph



#Running the app
if __name__ == "__main__":
    app.run_server()