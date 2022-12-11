import pandas as pd
import seaborn as sns
import matplotlib as plt

df = pd.read_csv("ICA2/resources/covid-data.csv")  # Creating a dataframe

# Renaming columns to more convinient names
df.rename({"new_cases": "New cases", "new_deaths": "New deaths",
          "location": "Country"}, axis=1, inplace=True)
# I am not going to lowercase countries, as 

# Deleting rows with null values from colum "continent". There rows are not valid locations
df = df.dropna(axis = 0, subset = ['continent'])

# Converting column "date" into date/time format.
df["date"] = pd.to_datetime(df["date"])

# We can also delete the rows in column "iso_code" that start with "OWID". They are not valid locations, as they don't have valid iso_code, such as "Wales", "Scotland".
df = df[~df["iso_code"].astype(str).str.startswith('OWID')]

# For some small islands in Oceania we don't have any data. We also don't have any data for such countries as Turkmenistan, North Korea, etc. Let's delete them.
# We can do it with for cycle ?
locations_todrop = ["Turkmenistan", "Tuvalu", "North Korea", "Niue", "Nauru", "Tonga", "Micronesia", "Marshall Islands",
                    "Anguilla", "Jersey", "Guam", "Guernsey", "United States Virgin Islands"]
for location in locations_todrop:
    df = df[~df["Country"].astype(str).str.startswith(location)]

# Determining the number of NaNs in data frame
nans_cases = df['New cases'].isnull().sum()
nans_deaths = df['New deaths'].isnull().sum()

# Determining the percent of NaNs in New Cases and New deaths column
rows_number = len(df.index)
nans_percent_cases = nans_cases / rows_number * 100
nans_percent_deaths = nans_deaths / rows_number * 100
print(nans_percent_cases, nans_percent_deaths)

# Creating new column in which we store month of the year.
df['Month'] = pd.to_datetime(df['date']).dt.to_period('M')

# Optimizing dataset by leaving only necessary columns
# Defining variable in which we store columns that we don't need.
to_leave = ["Country", "New cases", "New deaths", "date", "Month", "continent"]
df = df[to_leave]  # Leaving only selected columns.


print(df.head(10))  # We look at the first five entries using "head" method
# print(df.info())

df.to_csv("data-cleaned.csv")  # Exporting cleaned data into the new file
