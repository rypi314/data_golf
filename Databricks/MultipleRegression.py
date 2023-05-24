# Databricks notebook source
import pandas as pd

# COMMAND ----------

df = spark.read.table('golfanalysis.training')

# COMMAND ----------

display(df.head(n=100))

# COMMAND ----------

# MAGIC %md
# MAGIC Remove the date features.

# COMMAND ----------

df = df['Course', 'NumHoles', 'OverPar', 'Score', 'Putts', 'GIRPerc', 'FairwayHitPerc', 'TemperatureAverage', 'WindSpeed']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Training

# COMMAND ----------

from sklearn.model_selection import train_test_split
from mlflow.tracking import MlflowClient
import lightgbm as lgb
import mlflow
from sklearn.metrics import accuracy_score
from urllib.parse import urlparse


# Load the TrainingSet into a dataframe which can be passed into sklearn for training a model
#training_df = training_set.load_df()

# End any existing runs (in the case this notebook is being run for a second time)
mlflow.end_run()

# Start an mlflow run, which is needed for the feature store to log the model
mlflow.start_run(run_name="golf_lgbm") 

data = df.toPandas()
data_dum = pd.get_dummies(data, drop_first=True)

# Extract features & labels
X = data_dum.drop(["OverPar"], axis=1)
y = data_dum.OverPar

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

lgb_params = {
            'n_estimators': 50,
            'learning_rate': 1e-3,
            'subsample': 0.27670395476135673,
            'colsample_bytree': 0.6,
            'reg_lambda': 1e-1,
            'num_leaves': 50, 
            'max_depth': 8, 
            }

mlflow.log_param("hyper-parameters", lgb_params)
lgbm_clf  = lgb.LGBMClassifier(**lgb_params)
lgbm_clf.fit(X_train,y_train)
lgb_pred = lgbm_clf.predict(X_test)

accuracy=accuracy_score(lgb_pred, y_test)
print('LightGBM Model accuracy score: {0:0.4f}'.format(accuracy_score(y_test, lgb_pred)))
mlflow.log_metric('accuracy', accuracy)

tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

# Model registry does not work with file store
if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(lgbm_clf, "GolfModel", registered_model_name="GolfModel")
else:
            mlflow.sklearn.log_model(lgbm_clf, "GolfModel")


mlflow.end_run()

# COMMAND ----------

import mlflow
logged_model = 'runs:/87cfdf4c855b4111908aee02e3465e2c/GolfModel'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
import pandas as pd
loaded_model.predict(pd.DataFrame(X))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC The gradient boosting model performed poorly so we will try a different approach.
