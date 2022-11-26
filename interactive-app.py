from dash import Dash, dcc, Output, Input #importing all of the necessary libraries. Output and Input is the part of the callback
import dash_bootstrap_components as dbc

#Building our components 
app = Dash(name = __name__, external_stylesheets = [dbc.themes.SKETCHY]) #Run the app and setup theme
my_text = dcc.Markdown(children = "  ")
my_input = dcc.Input(value = "хуй")

#Customizing the layout 
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([])
    ])
    ])

#Building a callback
#A callback decorator
@app.callback( 
    Output(my_text, component_property = "children"), #Output of the callback, Q: why do we need component property?
    Input(my_input, component_property = "value") #Input of the callback (interactive part). 
)

#A callback function that always should be after callback 
def update_title(user_input): #A function arguments come from the component property of the Input берет инпут
    return user_input + "хуй" #овзвращает в аутпут 

#Running the app
if __name__ == "__main__":
    app.run_server()



