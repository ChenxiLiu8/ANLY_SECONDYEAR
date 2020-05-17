import pandas as pd 
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import tree
import lightgbm as lgb
from multiprocessing import cpu_count
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
###### Read in the data set 
df = pd.read_csv("Final_Model_Building.csv")


df.dtypes

cancer_rate_type = []
for i in range(len(df)):
    if df['Time_Adjusted_Cancer_Rate'][i] <= 0.432:
        cancer_rate_type.append('Low')
    elif 0.432 < df['Time_Adjusted_Cancer_Rate'][i] < 0.472:
        cancer_rate_type.append('Medium')
    else:
        cancer_rate_type.append('High')
        
df['Cancer_Rate_Type'] = cancer_rate_type
    
##### make training and testing set
X = df.iloc[:,:-1]
y = df.iloc[:,9]

#### Drop columns
X = X.drop('County',axis = 1 )
X = X.drop('State', axis = 1 )
X = X.drop('Number_Of_NPL_Sites', axis = 1)
##X = X.drop('Number_Of_Harmful_Power_Plants', axis = 1)
X = X.drop('Time_Adjusted_Cancer_Rate',axis = 1)
trends = pd.get_dummies(X['Recent_5years_Trend'],drop_first = True)
X = X.drop('Recent_5years_Trend', axis = 1)
X = pd.concat([X,trends], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size  = 0.2, random_state = 0)


##### Logistic Regression 
logit = LogisticRegression(C=1, solver='lbfgs', max_iter=500,
                           random_state=17, n_jobs=4,
                          multi_class='multinomial')
logit_pipe = Pipeline([('scaler', StandardScaler()), 
                       ('logit', logit)])
logit_pipe.fit(X_train, y_train)
y_pred_lf = logit_pipe.predict(X_test)
score_lf = accuracy_score(y_test, y_pred_lf)

##### 0.41

##### Decision Tree
tree = tree.DecisionTreeClassifier()
tree.fit(X_train,y_train)
y_pred_tree = tree.predict(X_test)
score_tree = tree.score(X_test,y_test)


##### 0.38
##### Random Forest

forest = RandomForestClassifier(n_estimators=100, random_state=17, n_jobs=4)
forest.fit(X_train,y_train)
y_pred_forest = forest.predict(X_test)
S = accuracy_score(y_test, y_pred_forest)


##### 0.43
##### SVM
### Linear
from sklearn.svm import SVC
svc = OneVsRestClassifier(SVC()).fit(X_train, y_train)
y_pred_svc = svc.predict(X_test)
print('SVM:')
print(svc.score(X_test, y_test))
print(confusion_matrix(y_test, y_pred_svc, labels=['High', 'Medium', 'Low']))

###### 0.415

###### LightBGM


lgb_clf = LGBMClassifier(objective='multiclass',random_state=17,n_estimators = 90,n_job = 16)
lgb_clf.fit(X_train, y_train)
accuracy_score(y_test, lgb_clf.predict(X_test))



##### 0.4436

##### param tuning stage-1

param_grid = {'num_leaves': [7, 15, 31, 63], 
              'max_depth': [3, 4, 5, 6, -1]}
grid_searcher = GridSearchCV(estimator=lgb_clf, param_grid=param_grid, 
                             cv=10, verbose=1, n_jobs=16)
grid_searcher.fit(X_train, y_train)
grid_searcher.best_params_, grid_searcher.best_score_
accuracy_score(y_test, grid_searcher.predict(X_test))

####### 0。4982
##### param tuning stage-2
num_iterations = 500
lgb_clf2 = LGBMClassifier(objective='multiclass',random_state=17, max_depth=4, 
                          num_leaves=15, n_estimators=num_iterations,learning_rate=0.00464,
                          n_jobs=16)

param_grid2 = {'learning_rate': np.logspace(-3, 0, 10)}
grid_searcher2 = GridSearchCV(estimator=lgb_clf2, param_grid=param_grid2,
                               cv=10, verbose=1, n_jobs=16)
grid_searcher2.fit(X_train, y_train)
print(grid_searcher2.best_params_, grid_searcher2.best_score_)
lgb_clf2.fit(X_train, y_train)
y_pred = lgb_clf2.predict(X_test)
print(accuracy_score(y_test, y_pred))

######final_model accuracy: 0.5



print(confusion_matrix(y_test, y_pred, labels=['High', 'Medium', 'Low']))
from lightgbm import plot_importance
import matplotlib.pylab as plt
plt.figure(figsize=(12,16))
plot_importance(lgb_clf2)
plt.title('Feature Importance')
plt.show()