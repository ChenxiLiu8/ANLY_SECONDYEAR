import re
import pandas as pd
import numpy as np 


df = pd.read_csv("USA_CancerRates_All_ByCounty.csv")

####Check the data types for the data 

df.dtypes 

###### Seperate state and county 


county = []
state = []
for i in range(len(df)) :
    state_list = df["State"][i].split(",")
    if len(state_list) == 2:
        county.append("")
        state.append("USA Total")
        continue
    county.append(state_list[0])
    temp = state_list[1].split("(")
    state.append(temp[0])
    

df['State'] = state
df['county'] = county
new_fips = []
df = df.rename(columns = {" FIPS" : "FIPS"})
for i in range(len(df)):
    if len(str(df["FIPS"][i])) == 1:
        new_fips.append("00000")
        continue
    if len(str(df["FIPS"][i])) == 4:
        new_fips.append("0" + str(df["FIPS"][i]))
        continue
    new_fips.append(str(df["FIPS"][i]))
    
df["FIPS"] = new_fips



######## Case per 100k cleaning (only take the number and transform it to float)

df = df.rename(columns = {"Age-AdjustedCANCERcases_per100000" : "case_per_100k"})
case_per_100k = []
for i in range(len(df)):
    try:
        temp = float(df['case_per_100k'][i])
    except:
        temp_str = re.findall(r'-?\d+\.?\d*', df['case_per_100k'][i])
        temp = float(temp_str[0])
    case_per_100k.append(temp)
    
df['case_per_100k'] = case_per_100k



####### recent Trend Cleaning 

df = df.rename(columns = {"Recent 5-Year Tren in Incidence Rates" : "incidence_rate_trend"})
inci_rate = []
error = []
for i in range(len(df)):
    try:
        inci_rate.append(float(df['incidence_rate_trend'][i]))
    except:
        if df['incidence_rate_trend'][i] == '*':
            inci_rate.append(0)
        else:
            error.append(i)
            
#### error
#### Noticed the error is empty which means we do not have non-numerical value besides empty value 
upper = []
lower = []
error = []
for i in range(len(df)):
    try:
        upper.append(float(df['Upper 95% CI'][i]))
        lower.append(float(df['Lower 95%CI'][i]))
    except:
        if df['Upper 95% CI'][i] == '*':
            upper.append(0)
        if df['Lower 95%CI'][i] == '*':
            lower.append(0)
        else:
            error.append(i)


df = df.rename(columns = {"Lower 95%CI" : "Lower 95% CI"})          


df['Upper 95% CI'] = upper
df['Lower 95% CI'] = lower
df["incidence_rate_trend"] =  inci_rate
#### error
#### Noticed the error is empty which means we do not have non-numerical value besides empty value 

###### Recent_trend cleaning
recent = []
error = []
for i in range(len(df)):
    if df['Recent Trend'][i] == '*':
        recent.append('unknown')
    elif df['Recent Trend'][i] != 'falling' and df['Recent Trend'][i] != 'unknown' and df['Recent Trend'][i] != 'stable' and df['Recent Trend'][i] != 'rising':
        error.append(i)
        recent.append('error')
    else:
        recent.append(df['Recent Trend'][i])
####error 
#### Noticed the error is empty which means we do not have unexpected value besides empty value 
df['Recent Trend'] = recent 



###### Vaildate dataset 

df.dtypes

#### vaildate the number of cases 
correct = []
error = []
for i in range(len(df)):
    if df['Lower 95% Confidence Interval'][i] <= case_per_100k[i] <= df['Upper 95% Confidence Interval'][i]:
        correct.append(i)
    else:
        error.append(i)
#####Botice the value is error is empty which means the value are all vaild
#### vaildate the rate_trend 
correct = []
error = []
for i in range(len(df)):
    if df['Lower 95% CI'][i] <= inci_rate[i] <= df['Upper 95% CI'][i]:
        correct.append(i)
    else:
        error.append(i)
#####Botice the value is error is empty which means the value are all vaild
#### vaildate FIPS

df_fip = pd.read_csv("FIPS_Info.csv")
new_fips = []
for i in range(len(df_fip)):
    if len(str(df_fip["fips"][i])) == 1:
        new_fips.append("00000")
        continue
    if len(str(df_fip["fips"][i])) == 4:
        new_fips.append("0" + str(df_fip["fips"][i]))
        continue
    new_fips.append(str(df_fip["fips"][i]))
df_fip['fips'] = new_fips


####

match_dict = {}

for i in range(len(df_fip)):
    val = df_fip['name'][i] 
    state = df_fip['states'][i]
    match_dict[df_fip['fips'][i]] = [val,state]
    

#### Normalize county data and state data using fips given in the nrcs data set
    
normal_state_code = []
normal_county = []
error = []
for i in range(len(df)):
    if df['FIPS'][i] in match_dict.keys():
        normal_state_code.append(match_dict[df['FIPS'][i]][1])
        normal_county.append(match_dict[df['FIPS'][i]][0])
    else:
        if df['FIPS'][i] == "00000":
            normal_state_code.append("total")
            normal_county.append("total")
        else: 
            error.append(i)
            normal_state_code.append("error")
            normal_county.append("error")
            
print(error)     


##### Notice we won't able to find a match for index 1908 and 2464 according to our fips data 


df['State_Code'] = normal_state_code
df['county'] = normal_county   
   
####
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
error = []
normal_state = []
for i in range(len(normal_state_code)):
    if normal_state_code[i] in states.keys():
        normal_state.append(states[normal_state_code[i]])
    else: 
        normal_state.append('error')
        error.append(i)

#####Calculate the cancer rate based on cancer_case_per 100k

rate = []
for i in range(len(df)):
    rate.append(df['case_per_100k'][i]/100000)


df['Cancer_Rate'] = rate
###error
#### Error as expected 0, 1908, 2464
        
df['State'] = normal_state
df = df.drop(0).drop(1908).drop(2464)

####file output
df.to_csv("cancer_rate_data_cleaned.csv",index=False)