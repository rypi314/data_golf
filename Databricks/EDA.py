# Databricks notebook source
# MAGIC %md
# MAGIC ## Golf Analysis 
# MAGIC
# MAGIC Data is from the Hole19 app of my round history.
# MAGIC
# MAGIC **Must run CreateDatabase.py set up file first.**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definitions
# MAGIC
# MAGIC Table grain is at the round level.
# MAGIC
# MAGIC |Column Name|Description|
# MAGIC |---|---|
# MAGIC |Day|Date of round day|
# MAGIC |Month|Date of round month|
# MAGIC |Year|Date of round year|
# MAGIC |Course|Name of golf course|
# MAGIC |GameType|Number of holes and type of game played|
# MAGIC |OverPar|Number of strokes over par|
# MAGIC |Score|Total score (Score - OverPar = Par for the Course)|
# MAGIC |Putts|Total number of putts|
# MAGIC |GIRPerc|Greens hit in regulation as a percentage|
# MAGIC |FairwayHitPerc|Total percentage of fairways as a percentage|

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from golfanalysis.training

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from golfanalysis.training

# COMMAND ----------

# MAGIC %md
# MAGIC ### Check correlations between GIR and Putts

# COMMAND ----------

df = spark.read.table('golfanalysis.training')

# COMMAND ----------

df.corr('OverPar', 'Putts')

# COMMAND ----------

df.corr('OverPar', 'GIRPerc')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Correlations
# MAGIC
# MAGIC We can see the correlation between strokes over par and green in regulations is slightly negative. While I wouldn't say this is correlated, it is a good sanity check to understand that as my score goes down, the green in regulations go up. 
# MAGIC
# MAGIC My putts are correlated to scoring over par. The more putts I hit, my score goes up.
