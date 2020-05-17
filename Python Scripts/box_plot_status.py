####### for graphing box plot 


import pandas as pd 
import numpy as np
from scipy import stats
import random





df = pd.read_csv("Final_Model_Building.csv")

df.dtypes



harmful_type = []
num_harmful_type = []
npl_type = []
combine = []
for i in range(len(df)):
    if df['Number_Of_Harmful_Power_Plants'][i] == 0:
        harmful_type.append('No Harmful Powerplants')
    elif df['Number_Of_Harmful_Power_Plants'][i] == 1:
        harmful_type.append('One Harmful Powerplants')
    elif df['Number_Of_Harmful_Power_Plants'][i] == 2:
        harmful_type.append('Two Harmful Powerplants')
    elif df['Number_Of_Harmful_Power_Plants'][i] > 2:
        harmful_type.append('More Than Two Harmful Powerplants')
    
    if df['Number_Of_NPL_Sites'][i] == 0:
        npl_type.append('No NPL Sites')
    else:
        npl_type.append('Have NPL Sites')
    
    if df['Number_Of_Harmful_Power_Plants'][i] == 0:
        num_harmful_type.append('No Harmful Powerplants')
    else:
        num_harmful_type.append('Have Harmful Powerplants')
        
    if df['Number_Of_Harmful_Power_Plants'][i] > 0 and df['Number_Of_NPL_Sites'][i] > 0:
        combine.append('Have Both')
    elif df['Number_Of_Harmful_Power_Plants'][i] == 0 and df['Number_Of_NPL_Sites'][i] == 0:
        combine.append('Have None')
    else:
        combine.append('Have one type')
df['NPL_Status'] = npl_type
df['Powerplants_Status'] = harmful_type
df['Harmful_Powerplants_Status'] = num_harmful_type 
df['Combine_Affect'] = combine




###### hypothesis testing

df_both = df.loc[df['Combine_Affect'] == 'Have Both']
df_none = df.loc[df['Combine_Affect'] == 'Have None']

df_have_pp  = df.loc[df['Harmful_Powerplants_Status'] == 'Have Harmful Powerplants']
df_dont_have_pp = df.loc[df['Harmful_Powerplants_Status'] == 'No Harmful Powerplants']

df_have_npl = df.loc[df['NPL_Status'] == 'Have NPL Sites']
df_dont_have_npl = df.loc[df['NPL_Status'] == 'No NPL Sites']
len(df_both)
len(df_none)


np.random.seed(23456782)
both_sample = random.sample(set(df_both['Time_Adjusted_Cancer_Rate']),300)
both_none =   random.sample(set(df_none['Time_Adjusted_Cancer_Rate']),300)


np.random.seed(1234567823)
have_pp_sample = random.sample(set(df_have_pp['Time_Adjusted_Cancer_Rate']),300)
no_pp_sample =  random.sample(set(df_dont_have_pp['Time_Adjusted_Cancer_Rate']),300)

np.random.seed(1234561)
have_npl_sample =  random.sample(set(df_have_npl['Time_Adjusted_Cancer_Rate']),300)
no_npl_sample =  random.sample(set(df_dont_have_npl['Time_Adjusted_Cancer_Rate']),300)

#### test sd of the sample 
stats.levene(both_sample,both_none)
stats.levene(have_pp_sample,no_pp_sample)
stats.levene(have_npl_sample,no_npl_sample)

#####t-test 
print(stats.ttest_ind(both_sample,both_none,equal_var = False))
print(stats.ttest_ind(have_pp_sample,no_pp_sample,equal_var = False))
print(stats.ttest_ind(have_npl_sample,no_npl_sample,equal_var = False))












df.dtypes

len(df)


df.to_csv("Model_Building_FINAL_box.csv",index=False)


