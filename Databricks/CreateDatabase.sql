-- Databricks notebook source
-- MAGIC %md 
-- MAGIC # Set up database environment
-- MAGIC
-- MAGIC In this file, we will create a new database named **golfanalysis** and add table **hole19download** and **weather** to it.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Create Database

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import pandas as pd

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS GolfAnalysis;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Add Table from Hole19 Download

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC
-- MAGIC df = pd.read_csv('../data/Hole19Download.csv', header=None)
-- MAGIC
-- MAGIC df = pd.DataFrame(df.values.reshape(-1, 8), 
-- MAGIC                   columns=['Date','Course','GameType','OverPar','Score', 'Putts', 'GIRPerc', 'FairwayHitPerc'])
-- MAGIC
-- MAGIC df.head()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC try:
-- MAGIC   spark.createDataFrame(df).write.saveAsTable('golfanalysis.hole19download')
-- MAGIC except: print('table already exists')

-- COMMAND ----------

show tables from golfanalysis;

-- COMMAND ----------

select * from golfanalysis.hole19download limit 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Add Weather Table
