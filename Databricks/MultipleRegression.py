# Databricks notebook source
import pandas as pd

# COMMAND ----------

df = spark.read.table('golfanalysis.training')

# COMMAND ----------

display(df.head(n=100))

# COMMAND ----------

from sklearn.model_selection import train_test_split
from mlflow.tracking import MlflowClient
import lightgbm as lgb
import mlflow
from sklearn.metrics import accuracy_score

# Load the TrainingSet into a dataframe which can be passed into sklearn for training a model
#training_df = training_set.load_df()

# End any existing runs (in the case this notebook is being run for a second time)
mlflow.end_run()

# Start an mlflow run, which is needed for the feature store to log the model
mlflow.start_run(run_name="lgbm_feature_store") 

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

mlflow.end_run()

# COMMAND ----------

y_test
