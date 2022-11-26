from dash import Dash, dcc, Output, Input, html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px  # Library that allows you to build graphs
import dash_mantine_components as dmc

# Creating dataframe (incorporating data to the app)
df = pd.read_csv("ICA2/data-cleaned.csv")

# Building our components
# Selecting a theme and opening the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
my_title = dcc.Markdown(
    children="# App that analyses COVID-19 situation", )  # Making the title

# Making graphs components
# The figure is empty, there is nothing at the beginning
my_graph = dcc.Graph(figure={})
my_bar = dcc.Graph(figure=px.histogram(df, x="month_year", y="New cases",
                   color="continent", title="Cases distribution by continent for each month"))

# Making selection components
dropdown_cases = dcc.Dropdown(options=["New cases", "New deaths"],
                              value="New cases",  # Setting the initial value
                              clearable=False)  # Non-erasable

multi_select = dmc.MultiSelect(data=["North America", "Africa", "South America", "Europe", "Asia", "Oceania"],
                               value=["North America", "Africa",
                                      "South America", "Europe", "Asia", "Oceania"],
                               searchable=True,
                               clearable=True)

# Building layout of the app
app.layout = html.Div(children=[

    html.Div(children=[
        html.H3(children=my_title, style={"marginTop": "15px"}),
        html.H6(children="Pandemic overview 2020-2022",
                style={"marginBottom": "30px"}),
    ], style={'textAlign': 'center'}),
    
    html.Div(children=[
        html.Div(children=[
            my_graph
        ]),

        html.Div(children=[
            dbc.Row([
                dbc.Col([multi_select], width=8),
                dbc.Col([dropdown_cases], width=3)
            ], justify="center")
        ])

    ], style={"border": "1px solid #6f6f6f", "border-radius": "13px", "padding": "30px", "margin-bottom": "20px"}),
    html.Div(children=[
        html.Div(children=[
            my_bar
        ]),
    ], style={"border": "1px solid", "border-radius": "13px", "padding": "30px"}),

], style={"padding": "30px"})

# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([my_title], width = 6)
#     ], justify="left"),
#     dbc.Row([
#         dbc.Col([my_graph], width = 12)
#     ], justify="center"),
#     dbc.Row([
#         dbc.Col([multi_select], width = 7),
#         dbc.Col([dropdown_cases], width = 3)
#     ], justify="center"),
#     dbc.Row([
#         dbc.Col([my_bar], width = 11),
#     ], justify="left"),
#     ])


# Building a callback
# A callback decorator
@app.callback(
    Output(my_graph, "figure"),
    Input(dropdown_cases, component_property="value"),
    Input(multi_select, component_property="value")
)
# A callback function that should always go after a callback decorator
def update_graph(cases_input, continents_input):

    # df_filtered = df[df["year"] == int(year_input)]
    mask = df.continent.isin(continents_input)

    fig = px.line(df[mask], x="date", y=cases_input,
                  color="Country", title=cases_input + " by day")

    return fig  # Fig goes into the output -> my_graph


# Running the app
if __name__ == "__main__":
    app.run_server()
