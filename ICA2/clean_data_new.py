import pandas as pd
import numpy as np 

df = pd.read_csv("ICA2/covid-data.csv") #Creating a dataframe 

to_drop = ["reproduction_rate"]

df.drop(to_drop, inplace = True, axis=1) #Deleting selected columns. We write inplace=True to make changes directly to the object instead of a copy. 

df.rename({"new_cases": "New cases", "new_deaths": "New deaths", "location": "Country"}, axis = 1, inplace = True)

df["date"]= pd.to_datetime(df["date"])

df['Month'] = pd.to_datetime(df['date']).dt.to_period('M')



print(df.head(10)) #We look at the first five entries using "head" method
print(df.info())

df.to_csv("data-cleaned.csv")
