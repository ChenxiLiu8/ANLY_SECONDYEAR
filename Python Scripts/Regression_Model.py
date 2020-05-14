import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import statsmodels.formula.api as smf
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
from multiprocessing import cpu_count


###### Read in the data set 
df = pd.read_csv("Final_Model_Building.csv")




df.dtypes



######  

X = df.iloc[:,:-1]
y = df.iloc[:,8]

###### Drop the state and county column
X = X.drop('County',axis = 1 )
X = X.drop('State', axis = 1 )
X = X.drop('Number_Of_NPL_Sites', axis = 1)
X = X.drop('Number_Of_Harmful_Power_Plants', axis = 1)
##### Create dummy variables for the recent_5years_ trend 

trends = pd.get_dummies(X['Recent_5years_Trend'],drop_first = True)

X = X.drop('Recent_5years_Trend', axis = 1)

X = pd.concat([X,trends], axis = 1)


##### Spliting the dataset into the training set and the test set 

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size  = 0.2, random_state = 0)

regr = LinearRegression()
regr.fit(X_train,y_train)

y_pred = regr.predict(X_test)

score = r2_score(y_test,y_pred)

print(score)


######## The R squared for our test model is not acceptable so we go ahead to test some other model 



####### Decision Tree


clf = tree.DecisionTreeRegressor()
clf = clf.fit(X_train,y_train)
y_pred_tree = clf.predict(X_test)
score_tree = r2_score(y_test,y_pred_tree)
print(score_tree)


###### Random Forest 

rand_forest = RandomForestRegressor()
rand_forest.fit(X_train,y_train)
y_pred_forest = rand_forest.predict(X_test)
score_forest = r2_score(y_test,y_pred_forest)


###### light gbm 
data_train = lgb.Dataset(X_train,y_train)
data_eval = lgb.Dataset(X_test,y_test,reference = data_train)
params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}


gbm = lgb.train(params,
                data_train,
                num_boost_round=200,
                valid_sets=data_eval,
                early_stopping_rounds=5)
gbm.save_model('model.txt')

y_pred_light = gbm.predict(X_test, num_iteration=gbm.best_iteration)

score_light = r2_score(y_test,y_pred_light)


