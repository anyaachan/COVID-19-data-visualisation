from dash import Dash, dcc, Output, Input, html
import numpy as np
import json
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_mantine_components as dmc
import plotly.graph_objects as go


# Creating dataframe (incorporating data to the app)
df = pd.read_csv("ICA2/resources/data-cleaned.csv")

# Creating new variables and storing the sum of columns in them.
total_cases = df["new_cases"].sum()
total_deaths = df["new_deaths"].sum()

df2 = df.copy()

# Creating a dataframe for "continent" tab

df_continent = df.copy()
df_continent['date'] = pd.to_datetime(df_continent['date'])
df_continent = df_continent.groupby(["continent", "date"])[
    ["new_cases", "new_deaths"]].sum().reset_index()

df_continent.sort_values('date', inplace=True)

print(df_continent.info())
# Preparing a map for chloropleth graph
# Loading json file
world_path = "ICA2/resources/custom.geo.json"
with open(world_path) as f:
    geo_world = json.load(f)

# Making conversion list for countries which names in dataset doesn't match with names in json file
country_conversion_dict = {
    'United States of America': 'United States',
    "S. Sudan": "South Sudan",
    "Central African Rep.": "Central African Republic",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Dem. Rep. Congo": "Democratic Republic of Congo",
    "Bosnia and Herz.": "Bosnia and Herzegovina"
}

# Defining an empty list
countries_geo = []

# Creating database with sum of cases and deaths grouped by each month
df2 = df.groupby(["country", "Month"])['new_cases', "new_deaths"].sum()
# Resetting the index in order for it to be sequential.
df2 = df2.reset_index(drop=False)

# "Converting" cases count from linear to a logarithm scale.
df2['cases_color'] = df2['new_cases'].apply(np.log10)

max_log = df2['cases_color'].max()
max_val = int(max_log) + 1

# Creating variables in which we store values and ticks of color scale.
values = [i for i in range(max_val)]
ticks = [10**i for i in values]

# Looping through the countries in json file
for country in geo_world['features']:

    # We create a variable in which we store the name of the country from json file
    country_name = country['properties']['name']
    geometry = country['geometry']
    country_name = country_conversion_dict[country_name] if country_name in country_conversion_dict.keys(
    ) else country_name

    countries_geo.append({
        'type': 'Feature',
        'geometry': geometry,
        'id': country_name
    })
geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}

# Building our components
# Selecting a theme and opening the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Creating a title for the map
my_title = dcc.Markdown(
    children="# App that analyses COVID-19 situation")  # Making the title

# Making graphs components
# The figure is empty at the beginning because it is an interactive part of the application and the data will be passed from callback.
my_graph = dcc.Graph(figure={})
my_bar = dcc.Graph(figure=px.histogram(df, x="Month", y="new_cases",
                   color="continent", title="Cases distribution by continent for each month"))


# chor = px.choropleth_mapbox(
#     df2, geojson=geo_world_ok,
#     locations="country",
#     animation_frame="Month",
#     color="cases_color",
#     range_color=(0, max_log),
#     mapbox_style='open-street-map',
#     zoom=0.5,
#     center={'lat': 19, 'lon': 11},
#     opacity=0.6
# )

# chor.update_layout(
#     height=600,
#     coloraxis_colorbar={
#         'title': 'Confirmed people',
#         'tickvals': values,
#         'ticks': "outside"
#     }
# )
my_chor = dcc.Graph(figure={})

# Making selection components
dropdown_cases = dcc.Dropdown(options=["new_cases", "new_deaths"],
                              value="new_cases",  # Setting the initial value
                              clearable=False)  # Non-erasable

continents_select = dmc.Select(data=["North America", "Africa", "South America", "Europe", "Asia", "Oceania"],
                               searchable=True,
                               value=["Europe"],
                               nothingFound="No options found",
                               clearable=True)
                               
tabs = dmc.Tabs(id="tabs-graph",
                active=2,
                variant="outline",
                children=[
                    dmc.Tab(label="Country"),
                    dmc.Tab(label="Continent"),
                    dmc.Tab(label="World")
                ],
                )


# Building layout of the app
app.layout = html.Div(children=[

    html.Div(children=[
        html.H3(children=my_title, style={"marginTop": "15px"}),
        html.H6(children="Pandemic overview 2020-2022",
                style={"marginBottom": "30px"}),
    ], style={'textAlign': 'center'}),

    html.Div(children=[

        html.Div(children=[
            html.H3(children=total_cases, style={
                    'fontWeight': 'bold'}),
            html.Label('Total cases'),
        ], style={"border": "1px solid", "border-color": "rgb(200, 200, 200)", "border-radius": "5px",
                  "padding": "15px", "margin": "0px 20px 20px 0px"}),

        html.Div(children=[
            html.H3(children=total_deaths, style={
                    'fontWeight': 'bold'}),
            html.Label('Total deaths'),
        ], style={"border": "1px solid", "border-color": "rgb(200, 200, 200)", "border-radius": "5px",
                  "padding": "15px", "margin": "0px 20px 20px 0px"}),

    ], style={'display': 'flex', 'justify-content': 'start', 'width': '100%', 'flex-wrap': 'wrap'}),


    html.Div(children=[
        tabs,
        html.Div(
            children=[
                my_graph
            ]),

        html.Div(children=[
            dbc.Row([
                dbc.Col([continents_select], width=8),
                dbc.Col([dropdown_cases], width=3)
            ], justify="center")
        ])
    ], style={"border": "1px solid", "border-color": "rgb(200, 200, 200)", "border-radius": "5px",
              "padding": "30px", "margin-bottom": "20px",
              'backgroundColor': 'rgb(255, 255, 255)'}),

    html.Div(children=[
        html.Div(children=[
            my_chor
        ]),
    ], style={"border": "1px solid", "border-color": "rgb(200, 200, 200)", "border-radius": "5px", "padding": "30px", 'backgroundColor': 'rgb(255, 255, 255)'}),
], style={"padding": "30px"})

# Building a callback
# A callback decorator


@app.callback(
    Output(my_graph, "figure"),
    Input(dropdown_cases, component_property="value"),
    Input(continents_select, component_property="value"),
)
# A callback function that should always go after a callback decorator
def update_graph(cases_input, continents_input):

    mask = df["continent"].isin(continents_input)
    fig = px.line(df_continent[mask], x="date",
                  y=cases_input, color_discrete_sequence=["#ff97ff"])

    fig.update_traces(opacity=0.3)
    help_fig = px.scatter(df_continent[mask], x="date", y=cases_input,
                          trendline="rolling", trendline_options=dict(window=14))
    x_trend = help_fig["data"][1]['x']
    y_trend = help_fig["data"][1]['y']

    fig.add_trace(go.Line(x=x_trend, y=y_trend))

    return fig  # Fig goes into the output -> my_graph


# Running the app
if __name__ == "__main__":
    app.run_server()
