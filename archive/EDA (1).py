# Databricks notebook source
# MAGIC %md
# MAGIC ## Golf Analysis 
# MAGIC
# MAGIC Data is from the Hole19 app of my round history.

# COMMAND ----------

# Golf Analysis from Hole19 data.

import pandas as pd
import numpy as np

df = pd.read_csv('../data/Hole19Download.csv', header=None)

df = pd.DataFrame(df.values.reshape(-1, 8), 
                  columns=['Date','Course','GameType','OverPar','Score', 'Putts', 'GIRPerc', 'FairwayHitPerc'])

df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definitions
# MAGIC
# MAGIC Table grain is at the round level.
# MAGIC
# MAGIC |Column Name|Description|
# MAGIC |---|---|
# MAGIC |Date|Date of round|
# MAGIC |Course|Name of golf course|
# MAGIC |GameType|Number of holes and type of game played|
# MAGIC |OverPar|Number of strokes over par|
# MAGIC |Score|Total score (Score - OverPar = Par for the Course)|
# MAGIC |Putts|Total number of putts|
# MAGIC |GIRPerc|Greens hit in regulation as a percentage|
# MAGIC |FairwayHitPerc|Total percentage of fairways as a percentage|

# COMMAND ----------

# create a new column 'new_column_name' based on the text of 'old_column_name'
df = df.assign(NumHoles=df['GameType'].str[:2])

# COMMAND ----------

df.head()

# COMMAND ----------

df = df[df.OverPar != "E"]

df['GIRPerc'] = list(map(lambda x: x[:-1], df['GIRPerc'].values))
df['FairwayHitPerc'] = list(map(lambda x: x[:-1], df['FairwayHitPerc'].values))

# convert column "a" of a DataFrame
df["OverPar"] = pd.to_numeric(df["OverPar"])
df["Score"] = pd.to_numeric(df["Score"])
df["Putts"] = pd.to_numeric(df["Putts"])
df["GIRPerc"] = pd.to_numeric(df["GIRPerc"])
df["FairwayHitPerc"] = pd.to_numeric(df["FairwayHitPerc"])
df["NumHoles"] = pd.to_numeric(df["NumHoles"])

df = df[df.OverPar > 0]

# COMMAND ----------

df.head()

# COMMAND ----------

df.count()

# COMMAND ----------

df.describe()

# COMMAND ----------


df.NumHoles.unique()

# COMMAND ----------

df.dtypes


# COMMAND ----------

#calculate quartiles for each numeric column in DataFrame
df.quantile(q=[0.25, 0.5, 0.75], axis=0, numeric_only=True)

# COMMAND ----------

df.tail()

# COMMAND ----------

dfplot = pd.DataFrame(df.groupby('Course').OverPar.mean())

# COMMAND ----------

import plotly.express as px
fig = px.bar(dfplot)
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Check correlations between GIR and Putts

# COMMAND ----------

df.corr()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Correlations
# MAGIC
# MAGIC We can see the correlation between strokes over par and green in regulations is slightly negative. While I wouldn't say this is correlated, it is a good sanity check to understand that as my score goes down, the green in regulations go up. 
# MAGIC
# MAGIC My putts are correlated to scoring over par. The more putts I hit, my score goes up.

# COMMAND ----------

df.head()

# COMMAND ----------

# MAGIC %pip install -r ./requirements.txt

# COMMAND ----------

# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)

# Create Point for Vancouver, BC
location = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Daily(location, start, end)
data = pd.DataFrame(data.fetch())

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()

# COMMAND ----------

df.head()

# COMMAND ----------

data.reset_index(level=0, inplace=True)

data.head()

# COMMAND ----------

pd.concat([df, data.reindex(df.index)], axis=1)

# COMMAND ----------

print (pd.merge(df, data, left_on='Date', right_on='time', how='left').drop('id1', axis=1))

# COMMAND ----------

pd.DataFrame(data)

# COMMAND ----------

df18 = df[df['NumHoles'] > 10]
df9 = df[df['NumHoles'] <= 10]

# COMMAND ----------

df18.head()

# COMMAND ----------

def CourseAverage(df):
        if df[df['NumHoles']] == 9:
                df = pd.DataFrame(df.groupby('Course').OverPar.mean())
                df['HoleNum'] == 9
        else:
                df = pd.DataFrame(df.groupby('Course').OverPar.mean())
                df['HoleNum'] == 18
        print(df)

# COMMAND ----------

dfplot9.head()

# COMMAND ----------

df['18HoleFlag'] = np.where(df['NumHoles'] > 10, True, False)

# COMMAND ----------

df = pd.DataFrame(df.groupby(['Course', 'NumHoles', '18HoleFlag']).OverPar.mean())

# COMMAND ----------

df.head()

# COMMAND ----------

import plotly.express as px

df = df
fig = px.bar(df, x='Course', y='OverPar',
             hover_data=['GameType', 'Putts'], color='18HoleFlag',
             labels={'OverPar':'Strokes over par'}, height=400)
fig.show()

# COMMAND ----------

import plotly.express as px

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.bar(df, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='country',
             labels={'pop':'population of Canada'}, height=400)
fig.show()

# COMMAND ----------

df.head()

# COMMAND ----------

import plotly.express as px

df = dfplot
fig = px.bar(df, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='country',
             labels={'pop':'population of Canada'}, height=400)
fig.show()
