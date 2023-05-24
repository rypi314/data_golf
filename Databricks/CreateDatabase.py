# Databricks notebook source
# MAGIC %md 
# MAGIC # Set up database environment
# MAGIC
# MAGIC In this file, we will create a new database named **golfanalysis** and add table **hole19download** and **weather** to it.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Database

# COMMAND ----------

import pandas as pd

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS GolfAnalysis;

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Add Table from Hole19 Download

# COMMAND ----------

df = pd.read_csv('../data/Hole19Download.csv', header=None)

df = pd.DataFrame(df.values.reshape(-1, 8), 
                  columns=['Date','Course','GameType','OverPar','Score', 'Putts', 'GIRPerc', 'FairwayHitPerc'])

df.head()

# COMMAND ----------

try:
  spark.createDataFrame(df).write.saveAsTable('golfanalysis.hole19download')
except: print('table already exists')

# COMMAND ----------

# MAGIC %sql
# MAGIC show tables from golfanalysis;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from golfanalysis.hole19download limit 5;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add Weather Table

# COMMAND ----------

# MAGIC %md
# MAGIC Uncomment the next cell if you need to install meteostat.

# COMMAND ----------

#%pip install -r ./requirements.txt

# COMMAND ----------

# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2022, 1, 1)
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

# MAGIC %md
# MAGIC Temperatures are in celsius.

# COMMAND ----------

data.reset_index(level=0, inplace=True)

data.head()

# COMMAND ----------

try:
  spark.createDataFrame(data).write.saveAsTable('golfanalysis.weather')
except: print('table already exists')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Features
# MAGIC
# MAGIC Create handful of additional features and join to make a training set.

# COMMAND ----------

# MAGIC %sql 
# MAGIC drop table if exists golfanalysis.weatherfeatures
# MAGIC ;
# MAGIC
# MAGIC create table golfanalysis.weatherfeatures
# MAGIC as
# MAGIC select *
# MAGIC , date_format(time, 'dd') as Day
# MAGIC , case 
# MAGIC           when date_format(time, 'M') = 1 then 'Jan'
# MAGIC           when date_format(time, 'M') = 2 then 'Feb'
# MAGIC           when date_format(time, 'M') = 3 then 'Mar'
# MAGIC           when date_format(time, 'M') = 4 then 'Apr'
# MAGIC           when date_format(time, 'M') = 5 then 'May'
# MAGIC           when date_format(time, 'M') = 6 then 'Jun'
# MAGIC           when date_format(time, 'M') = 7 then 'Jul'
# MAGIC           when date_format(time, 'M') = 8 then 'Aug'
# MAGIC           when date_format(time, 'M') = 9 then 'Sep'
# MAGIC           when date_format(time, 'M') = 10 then 'Oct'
# MAGIC           when date_format(time, 'M') = 11 then 'Nov'
# MAGIC           when date_format(time, 'M') = 12 then 'Dec'
# MAGIC           else null end as Month
# MAGIC , date_format(time, 'y') as Year
# MAGIC from golfanalysis.weather
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC show columns from golfanalysis.hole19features

# COMMAND ----------

# MAGIC %sql 
# MAGIC drop table if exists golfanalysis.hole19features
# MAGIC ;
# MAGIC
# MAGIC create table golfanalysis.hole19features
# MAGIC as
# MAGIC select 
# MAGIC   Date
# MAGIC   , Course
# MAGIC   , GameType
# MAGIC   , cast(substring(GameType FROM 1 FOR 2) as int) as NumHoles
# MAGIC   , cast(OverPar as int) as OverPar
# MAGIC   , cast(Score as int) as Score
# MAGIC   , cast(Putts as int) as Putts
# MAGIC   , cast(replace(GIRPerc, '%', '') as int) as GIRPerc
# MAGIC   , cast(replace(FairwayHitPerc, '%', '') as int) as FairwayHitPerc 
# MAGIC   , substring(Date FROM 1 FOR 2) as Day
# MAGIC   , substring(Date FROM 4 FOR 3) as Month
# MAGIC   , substring(Date, -4) as Year
# MAGIC from golfanalysis.hole19download
# MAGIC where OverPar > 0 --Remove bad data that saved automatically 
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from golfanalysis.weatherfeatures

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from golfanalysis.hole19features

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from golfanalysis.weatherfeatures
# MAGIC where Day = 9
# MAGIC and Month = 5 
# MAGIC and Year = 2023
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists golfanalysis.training
# MAGIC ;
# MAGIC
# MAGIC create table golfanalysis.training
# MAGIC as
# MAGIC select 
# MAGIC   h19.Day
# MAGIC   , h19.Month
# MAGIC   , h19.Year
# MAGIC   , h19.Course
# MAGIC   , h19.NumHoles
# MAGIC   , h19.OverPar
# MAGIC   , h19.Score
# MAGIC   , h19.Putts
# MAGIC   , h19.GIRPerc
# MAGIC   , h19.FairwayHitPerc
# MAGIC   , wf.tavg as TemperatureAverage
# MAGIC   , wf.wspd as WindSpeed
# MAGIC from golfanalysis.hole19features h19
# MAGIC   left join golfanalysis.weatherfeatures wf 
# MAGIC     on h19.Day = wf.Day 
# MAGIC     and h19.Month = wf.Month 
# MAGIC     and h19.Year = wf.Year
# MAGIC   limit 100
# MAGIC ;
