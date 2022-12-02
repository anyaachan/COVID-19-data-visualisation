import pandas as pd

df = pd.read_csv("ICA2/resources/covid-data.csv")  # Creating a dataframe

# Renaming columns to more convinient names
df.rename({"new_cases": "New cases", "new_deaths": "New deaths",
          "location": "Country"}, axis=1, inplace=True)

# Deleting rows with null values from colum])
df = df.dropna(axis=0, subset=['continent'])

# Converting column "date" into date/time format.
df["date"] = pd.to_datetime(df["date"])

# Creating new column in which we store month of the year.
df['Month'] = pd.to_datetime(df['date']).dt.to_period('M')

# Optimizing dataset by leaving only necessary columns
# Defining variable in which we store columns that we don't need.
to_leave = ["Country", "New cases", "New deaths", "date", "Month", "continent"]
df = df[to_leave]  # Leaving only selected columns.

print(df.head(10))  # We look at the first five entries using "head" method
print(df.info())

df.to_csv("data-cleaned.csv")  # Exporting cleaned data into the new file
