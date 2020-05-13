import pandas as pd
import numpy as np 




####### read in the data file 
df_standard = pd.read_csv("FIPS_Info.csv")
df_pp = pd.read_csv("Power_Plant_normalized.csv")
df_NPL = pd.read_csv("NPL_Site_normalized.csv")
df_Cancer = pd.read_csv("cancer_rate_data_cleaned.csv")


######## This script is use for generate a new data set for future model building 

df_pp.dtypes

fuel_type = set(df_pp['primary_fuel'])


###### According to some article and research we can classfied powerplants by harmful and non-harmful to human body( potential ) by their emission
#### Biomass-emission: https://www.pfpi.net/wp-content/uploads/2011/04/PFPI-biomass-carbon-accounting-overview_April.pdf  (Harmful)(300% more than coal)
#### Cogeneration: https://powering.mit.edu/cogeneration-sustainable-choice (harmful)
#### Geothermal: https://www.ucsusa.org/resources/environmental-impacts-geothermal-energy (Non-harmful)
#### Nuclear: https://www.nrc.gov/about-nrc/radiation/related-info/faq.html (Harmful)
#### Waste: https://en.wikipedia.org/wiki/Waste-to-energy_plant (Harmful)
#### Petcoke: http://priceofoil.org/content/uploads/2013/01/OCI.Petcoke.FINALSCREEN.pdf (Harmful)
#### Gas: Harmful 
#### Oil: Harmful 
#### Storage: Non-harmful
#### Wind : Non-harmful
#### Hydro: Non-harmful
#### Coal: Harmful 
#### Other(since it is a small percentage):Non-harmful


harmful_type = []
harmful = ['Biomass','Coal','Oil','Petcoke','Gas','Nuclear','Waste','Cogeneration']
non_harmful = ['Geothermal','Hydro','Other','Storage','Solar','Wind']
for i in range(len(df_pp)):
    if df_pp['primary_fuel'][i] in harmful:
        harmful_type.append('harmful')
    else:
        harmful_type.append('unharmful')
df_pp['harmful_type'] = harmful_type

#######  My plans :
#######  Dataset for model building will contains following information:
#######  1. County
#######  2. Number of NPL sites
#######  3. Total NPL score (sum)
#######  4. Number of 'harmful' powerplants
#######  5. incident rate trend 
#######  6. recent trend (categorical)
#######  7. cancer rate (Age adjusted)

####### create empty dictionary with county as keys and list as value the indexing of the list associated to the element above
dict_final= {}
for i in range(len(df_Cancer)):
    tuple_temp = (df_Cancer['county'][i],df_Cancer['State'][i])
    if tuple_temp not in dict_final.keys():
        dict_final[tuple_temp] = [0,0,0,None,None,None]
len(dict_final.keys())
###### get number of npl site and the total score into the list 
df_NPL.dtypes
for i in range(len(df_NPL)):
    tuple_temp  = (df_NPL['normalized_county'][i],df_NPL['State'][i])
    for key in dict_final.keys():
        if tuple_temp == key:
            dict_final[key][0] += 1
            dict_final[key][1] += df_NPL['Site Score'][i]
dict_final           

##### get number of harmful power plants into the list 
df_pp.dtypes
len(df_Cancer)
for i in range(len(df_pp)):
    tuple_temp  = (df_pp['normalized_county'][i],df_pp['state'][i])
    for key in dict_final.keys():
        if tuple_temp == key and df_pp['harmful_type'][i] == 'harmful':
            dict_final[key][2] += 1



#### get number other data 
df_Cancer.dtypes

for i in range(len(df_Cancer)):
    tuple_temp = (df_Cancer['county'][i],df_Cancer['State'][i])
    for key in dict_final.keys():
        if tuple_temp == key:
            dict_final[key][3] = df_Cancer['incidence_rate_trend'][i]
            dict_final[key][4] = df_Cancer['Recent Trend'][i]
            dict_final[key][5] = df_Cancer['Cancer_Rate'][i]
len(df_Cancer.loc[df_Cancer['Recent Trend'] == 'unknown'])


######### Produce data set 
county = []
num_NPL = []
score_sum = []
num_pp = []
inci_trend = []
recent_trend = []
cancer_rate = []
for key in dict_final.keys():
    ########## Since the unknown recent trend do not offer any information we will drop them in our model building process
    if dict_final[key][4] != 'unknown':
        county.append(key[0])
        num_NPL.append(dict_final[key][0])
        score_sum.append(dict_final[key][1])
        num_pp.append(dict_final[key][2])
        inci_trend.append(dict_final[key][3])
        recent_trend.append(dict_final[key][4])
        cancer_rate.append(dict_final[key][5]*100)

df_final = pd.DataFrame(list(zip(county,num_NPL,score_sum,num_pp,inci_trend,recent_trend,cancer_rate)),columns = ['County','Number_Of_NPL_Sites','NPL_Score_Sum',\
                             'Number_Of_Harmful_Power_Plants','Incident_Rate_Trend','Recent_5years_Trend','Time_Adjusted_Cancer_Rate'])
    
df_final.to_csv("Final_Model_Building.csv",index=False)
