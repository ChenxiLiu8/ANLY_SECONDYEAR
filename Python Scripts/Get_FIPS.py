##### This code is to get matching FIPS for each county
import pandas as pd 
import numpy as np 



##### Read in the normalized data set 

df_standard = pd.read_csv("FIPS_Info.csv")
df_cancer = pd.read_csv('cancer_rate_data_cleaned.csv')
df_NPL = pd.read_csv('NPL_Site_normalized.csv')
df_pp = pd.read_csv('Power_Plant_normalized.csv')

cancer_fips = []
npl_fips = []
pp_fips = []
df_standard.dtypes
df_cancer.dtypes
df_NPL.dtypes
for i in range(len(df_cancer)):
    for j in range(len(df_standard)):
        if df_cancer['county'][i] == df_standard['name'][j] and df_cancer['State_Code'][i] == df_standard['states'][j]:
            cancer_fips.append(df_standard['fips'][j])
len(df_cancer)
len(cancer_fips)

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
state_name = []
for i in range(len(df_standard)):
    if df_standard['states'][i] in states.keys():
        state_name.append(states[df_standard['states'][i]])
df_standard['state name'] = state_name


for i in range(len(df_NPL)):
    for j in range(len(df_standard)):
        if df_NPL['normalized_county'][i] == df_standard['name'][j] and df_NPL['State'][i] == df_standard['state name'][j]:
            npl_fips.append(df_standard['fips'][j])
len(df_NPL)
len(npl_fips)
for i in range(len(df_pp)):
    for j in range(len(df_standard)):
        if df_pp['normalized_county'][i] == df_standard['name'][j] and df_pp['state'][i] == df_standard['state name'][j]:
            pp_fips.append(df_standard['fips'][j])
            
len(df_pp)
len(pp_fips)    


df_cancer['Fips'] = cancer_fips
df_pp['Fips'] = pp_fips
df_NPL['Fips'] = npl_fips

df_NPL.to_csv("NPL_Site_FINAL.csv",index=False)
df_pp.to_csv("Power_Plants_FINAL.csv",index=False)
df_cancer.to_csv("Cancer_Rate_FINAL.csv",index=False)
df_standard.to_csv("FIPS_FINAL.csv",index=False)