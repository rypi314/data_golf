-- Databricks notebook source
-- MAGIC %md 
-- MAGIC ## Set up database environment
-- MAGIC
-- MAGIC Before you begin, upload the hole19down file to the default databricks databasea as **hole_19_download**.

-- COMMAND ----------

create database GolfAnalysis;

-- COMMAND ----------

show databases;

-- COMMAND ----------

show tables from default;

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

select * from hole_19_download limit 5;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC df = spark.read.table('default.hole_19_download')

-- COMMAND ----------

-- MAGIC %python 
