##### This part of code is to extract useful information from the powerplant and NPL data and normalized the county so that all the data sets using the same county set 
import pandas as pd
import numpy as np


#### cancer_rate's county is already been normalized 




### now we normalize the county_data in power-plants data set

####read in the standard county name that is in fips data set

df_standard = pd.read_csv("FIPS_Info.csv")
df_pp = pd.read_csv("power_plants_cleaned.csv")


city_behind = []
#### extract city name in the county variables of standard data set

for i in range(len(df_standard)):
    list_temp = df_standard['name'][i].split(" ")
    if list_temp[len(list_temp)-1] == "City":
        if list_temp[0] == "St" or list_temp[0] == "St.":
            list_temp[0] = "Saint"       
        str_app = " ".join(list_temp[:len(list_temp)-1])
        city_behind.append(str_app)
    else:
        if list_temp[0] == "St" or list_temp[0] == "St.":
            list_temp[0] = "Saint" 
        str_app = " ".join(list_temp)
        city_behind.append(str_app)
        
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
states_name = []
for i in range(len(df_standard)):
    if df_standard['states'][i] in states:
        states_name.append(states[df_standard['states'][i]])
df_standard["states_name"] = states_name


normal_county_pp = []
for i in range(len(df_pp)):
    app_list = []
    for j in range(len(city_behind)):
        if str(city_behind[j]) in str(df_pp['county'][i]) and str(df_standard['states_name'][j]) == str(df_pp['state'][i]):
            app_list.append(df_standard['name'][j])
    if len(app_list) == 0:
        normal_county_pp.append("unmatched")
    else:
        normal_county_pp.append(app_list[0])

df_pp["normalized_county"] = normal_county_pp

df_unmatched = df_pp.loc[df_pp['normalized_county'] == "unmatched"]
len(df_unmatched)
len(df_pp)
######### Only a small portion of the rows are unmatched to the standard county,I decide to drop them

drop_list = df_pp.index[df_pp['normalized_county'] == "unmatched"].tolist()

######## Drop Associate index 
for index in drop_list:
    df_pp = df_pp.drop(index)



######## file output


output_header_pp = ['country','name','capacity_mw','latitude','longitude','primary_fuel','commissioning_year','state','normalized_county',
                    'generation_gwh_2013','generation_gwh_2014','generation_gwh_2015','generation_gwh_2016','generation_gwh_2017'\
                    ]

df_pp.to_csv("Power_Plant_normalized.csv",index=False,columns = output_header_pp)


####### Normalized the NPL data set 
#######
#######
df_NPL = pd.read_csv("Superfund National Priorities List (NPL) Sites with Status Information.csv")

##### Change st and st. to saint 
temp = []
for i in range(len(df_NPL)):
    list_temp = df_NPL['County'][i].split(" ")
    if list_temp[0] == "St" or list_temp[0] == "St.":
        list_temp[0] = 'Saint'
    str_app = " ".join(list_temp)
    temp.append(str_app)

df_NPL['County'] = temp

NPL_county = []
for i in range(len(df_NPL)):
    comma_list = df_NPL['County'][i].split(",")
    temp_element = comma_list[0]
    app_list = []
    for j in range(len(city_behind)):
        if str(city_behind[j]) in str(temp_element) and str(df_standard['states_name'][j]) == str(df_NPL['State'][i]):
            app_list.append(df_standard['name'][j])
    
    if len(app_list) == 0:
        NPL_county.append('unmatched')
    else:
        NPL_county.append(app_list[0])
df_NPL['normalized_county'] = NPL_county

df_unmatched = df_NPL.loc[df_NPL['normalized_county'] == "unmatched"]

drop_list_NPL_county = df_NPL.index[df_NPL['normalized_county'] == "unmatched"].tolist()
drop_list_NPL_NPL_Site = df_NPL.index[df_NPL['Status'] != "NPL Site"].tolist()
drop_list_NPL = list(set(drop_list_NPL_county) | set(drop_list_NPL_NPL_Site))
######### 
######### Only a small portion of the rows are unmatched to the standard county,I decide to drop them


####### Drop Associated Rows

for index in drop_list_NPL:
    df_NPL = df_NPL.drop(index)
    

#### file output
output_header = ['Site Name','Site Score','State','normalized_county','Status','Latitude','Longitude']
df_NPL.to_csv("NPL_Site_normalized.csv",index=False,columns = output_header)
