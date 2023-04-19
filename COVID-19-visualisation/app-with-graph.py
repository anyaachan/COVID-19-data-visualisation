from dash import Dash, dcc, Output, Input, html
import numpy as np
import json
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_mantine_components as dmc
import plotly.graph_objects as go
import locale

# Preparation of the data
# Setting numeric format to the US format in order to separate thousands using comma.
locale.setlocale(locale.LC_NUMERIC, 'en_US')

# Creating dataframe in order to incorporate data to the app.
df = pd.read_csv("ICA2/resources/data-cleaned.csv")

# Creating new variables and storing the sum of values in columns in them.
total_cases = df["new_cases"].sum()
total_deaths = df["new_deaths"].sum()

# Creating a dataframe for "continent" tab
df_continent = df.copy()
# Converting the date column to the datetime format
df_continent['date'] = pd.to_datetime(df_continent['date'])
# Grouping the data in the dataset to obtain the sum of daily new cases and deaths for each continent.
df_continent = df_continent.groupby(["continent", "date"])[
    ["new_cases", "new_deaths"]].sum().reset_index()
df_continent.sort_values('date', inplace=True)

# Creating a dataframe for "country" tab
df_country = df.copy()
# Converting the date column to the datetime format
df_country['date'] = pd.to_datetime(df_country['date'])
df_country.sort_values('date', inplace=True)

# Creating a dataframe for "world" tab
df_world = df.copy()
# Converting the date column to the datetime format
df_world['date'] = pd.to_datetime(df_world['date'])
# Grouping the data in the dataset to obtain the sum of daily new cases and deaths in the world.
df_world = df.groupby(["date"])[
    ["new_cases", "new_deaths"]].sum().reset_index()
df_world['date'] = pd.to_datetime(df_world['date'])
df_world.sort_values('date', inplace=True)

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

# Defining an empty list in which we will store the informattion about the countries.
countries_geo = []

# Creating a dataframe with sum of cases and deaths grouped by each month
df2 = df.copy()
df2 = df.groupby(["country", "Month"])['new_cases', "new_deaths"].sum()
# Resetting the index in order for it to be sequential.
df2 = df2.reset_index(drop=False)

# "Converting" cases color count from linear to a logarithmic scale.
df2['cases_color'] = df2['new_cases'].apply(np.log10)

# Creating a variable and storing a maximum value of cases in it. It will help us with the color scale in choropleth map
max_log = df2['cases_color'].max()
max_val = int(max_log) + 1

# Creating variables in which we store values and ticks of color scale.
values = [i for i in range(max_val)]
ticks = [locale.format("%d", 10**i, grouping=True) for i in values]

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
    children="# Covid-19 Pandemic Analysis")  # Making the title

# Making graphs components
# The figure is empty at the beginning because it is an interactive part of the application and the data will be passed from callback.
my_graph = dcc.Graph(figure={})
my_bar = dcc.Graph(figure=px.histogram(df, x="Month", y="new_cases",
                   color="continent", title="Cases distribution by continent for each month"))

# Creating a choropleth map graph
chor = px.choropleth_mapbox(
    df2, geojson=geo_world_ok,
    locations="country",
    animation_frame="Month",
    color="cases_color",
    range_color=(0, max_log),
    mapbox_style='open-street-map',
    zoom=0.5,
    center={'lat': 19, 'lon': 11},
    opacity=0.6
)

# Updating a choropleth map color bar
chor.update_layout(
    height=600,
    coloraxis_colorbar={
        'title': 'Confirmed cases, people',
        'tickvals': values,
        'ticktext': ticks,
        'ticks': "outside"
    }
)

my_chor = dcc.Graph(figure=chor)

# Creating dropdown selection so the user will be able to switch between the New cases and New deaths values.
dropdown_cases = dcc.Dropdown(options=[{"value": "new_cases", "label": "New Cases"},
                                       {"value": "new_deaths", "label": "New Deaths"}],
                              value="new_cases",  # Setting the initial value
                              clearable=False)  # Non-erasable

# Creating dropdown selection so the user will be able to switch between the continents.
continents_select = dmc.Select(data=["North America", "Africa", "South America", "Europe", "Asia", "Oceania"],
                               searchable=True,
                               value="Europe",
                               nothingFound="No options found",
                               clearable=True)

# Creating tabs to switch between the data for the country, continent or world.
tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Country", value="Country"),
                dmc.Tab("Continent", value="Continent"),
                dmc.Tab("World", value="World")
            ]
        ),
    ],
    value="Continent",
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
            html.H3(children=locale.format("%d", total_cases, grouping=True),  style={
                    'fontWeight': 'bold'}),
            html.Label('Total cases'),
        ], style={"border": "1px solid", "border-color": "rgb(200, 200, 200)", "border-radius": "5px",
                  "padding": "15px", "margin": "0px 20px 20px 0px"}),

        html.Div(children=[
            html.H3(children=locale.format("%d", total_deaths, grouping=True), style={
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

# Building the first callback which will pass the dropdown data to the second callback

@app.callback(
    [Output(continents_select, component_property="data"),
     Output(continents_select, component_property="value")],
    Input(tabs, component_property="value")
)
def update_select(tabs_input):
    if tabs_input == "Continent":
        data = ["North America", "Africa",
                "South America", "Europe", "Asia", "Oceania"]
        value = "Europe"
        return data, value
    if tabs_input == "Country":
        data = df["country"].unique().tolist()
        value = "Czechia"
        return data, value
    else:
        data = ["World"]
        value = "World"
        return data, value

# The second callback in which we'll recieve the information from the first callback and make graphs depending what we'll recieve.

@app.callback(
    Output(my_graph, "figure"),
    Input(dropdown_cases, component_property="value"),
    Input(continents_select, component_property="value"),
    Input(tabs, component_property="value")
)
# A callback function that should always go after a callback decorator
def update_graph(cases_input, continents_input, tabs_input):
    # Defining a function with which we will update x and y axeses titles.
    def update_title(fig):
        if cases_input == "new_cases":
            fig.update_yaxes(title="New cases count, people")
        else:
            fig.update_yaxes(title="New deaths count, people")

    # Defining a function with which we will add a trace for average and update it.
    def update_traces(fig, mask):
        fig.update_traces(opacity=0.4)
        help_fig = px.scatter(mask, x="date", y=cases_input,
                              trendline="rolling", trendline_options=dict(window=14, center=True))
        x_trend = help_fig["data"][1]['x']
        y_trend = help_fig["data"][1]['y']

        fig.add_trace(go.Line(x=x_trend, y=y_trend, name="14-day average", connectgaps=True))
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(title="Date")

    if tabs_input == "Continent":

        mask = df_continent
        mask = df_continent.loc[df_continent['continent'] == continents_input]
        fig = px.line(mask, x="date",
                      y=cases_input)

        update_traces(fig, mask)
        update_title(fig)

        return fig  # Fig goes into the output -> my_graph

    elif tabs_input == "Country":
        mask = df_country.loc[df_country['country'] == continents_input]
        fig = px.line(mask, x="date",
                      y=cases_input)

        update_traces(fig, mask)
        update_title(fig)

        return fig

    elif tabs_input == "World":
        fig = px.line(df_world, x="date",
                      y=cases_input)
        update_traces(fig, df_world)
        update_title(fig)

        return fig  


# Running the app
if __name__ == "__main__":
    app.run_server()