import pandas as pd
import numpy as np 

df = pd.read_csv("ICA2/data.csv") #Creating a dataframe 

to_drop = ["countryterritoryCode",
            "popData2020",
            "geoId"]

df.drop(to_drop, inplace = True, axis=1) #Deleting selected columns. We write inplace=True to make changes directly to the object instead of a copy. 

df.rename({"countriesAndTerritories": "country", "continentExp": "continent"}, axis = 1, inplace = True) #Renaming columns to more convinient names


for i in range(df.shape[0]): 
  if df.cases.iloc[i] < 0.0: #Looking for the negative cases
        df.cases.iloc[i] = 20.0 #Replacing them with 1000

for i in range(df.shape[0]): 
  if df.deaths.iloc[i] < 0.0: #Looking for the negative deaths
        df.deaths.iloc[i] = 20.0 #Replacing them with 300

for i in range(df.shape[0]): 
  if df.deaths.iloc[i] > 5000.0: #Looking for absurd deaths
        df.deaths.iloc[i] = 20.0 #Replacing them with 300

df["dateRep"]= pd.to_datetime(df['dateRep'])
df = df.astype({"year" : "int"})

df = df.sort_values(by='dateRep')


print(df.head(10)) #We look at the first five entries using "head" method
print(df.info())

df.to_csv("data-cleaned.csv")
