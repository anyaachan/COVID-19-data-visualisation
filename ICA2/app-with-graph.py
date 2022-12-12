from dash import Dash, dcc, Output, Input, html
import numpy as np
import json
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px  
import dash_mantine_components as dmc

# Creating dataframe (incorporating data to the app)
df = pd.read_csv("ICA2/resources/data-cleaned.csv")

# Creating new variables and storing the sum of columns in them.
total_cases = df["new_cases"].sum()
total_deaths = df["new_deaths"].sum()

# "Converting" cases count from linear to a logarithm scale.
df['cases_color'] = df['new_cases'].apply(np.log2)
max_log = int(df['cases_color'].max())

# Creating variables in which we store values and ticks of color scale.
values = [i for i in range(max_log + 1)]
ticks = [i for i in values]

# Preparing a map for chloropleth graph
# Loading json file
world_path = "ICA2/resources/custom.geo.json"
with open(world_path) as f:
    geo_world = json.load(f)

# Making conversion list for counties which names in dataset doesn't match with names in json file
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
df2 = df2.reset_index(drop=False)

# Looping through the countries in json file
for country in geo_world['features']:

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
    children="# App that analyses COVID-19 situation", )  # Making the title

# Making graphs components
# The figure is empty at the beginning because it is an interactive part of the application and the data will be passed from callback.
my_graph = dcc.Graph(figure={})

my_bar = dcc.Graph(figure=px.histogram(df, x="Month", y="new_cases",
                   color="continent", title="Cases distribution by continent for each month"))


chor = px.choropleth_mapbox(
    df2, geojson=geo_world_ok,
    locations="country",
    color='new_cases',
    animation_frame="Month",
    range_color=(0, 7000000),
    mapbox_style='open-street-map',
    zoom=0.5,
    center={'lat': 19, 'lon': 11},
    opacity=0.6
)

chor.update_layout(
    height=600,
    coloraxis_colorbar={
        'title': 'Confirmed people',
        'tickvals': [0, 100000, 500000, 1000000, 4000000, 6000000],
        'ticks': "outside"
    }
)
my_chor = dcc.Graph(figure=chor)

# Making selection components
dropdown_cases = dcc.Dropdown(options=["new_cases", "new_deaths"],
                              value="new_cases",  # Setting the initial value
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

        html.Div(children=[
            my_graph
        ]),

        html.Div(children=[
            dbc.Row([
                dbc.Col([multi_select], width=8),
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
    Input(multi_select, component_property="value")
)
# A callback function that should always go after a callback decorator
def update_graph(cases_input, continents_input):

    mask = df.continent.isin(continents_input)

    fig = px.line(df[mask], x="date",
                  y=cases_input,
                  color="country",
                  title=cases_input + " by day"
                  )
    return fig  # Fig goes into the output -> my_graph


# Running the app
if __name__ == "__main__":
    app.run_server()
