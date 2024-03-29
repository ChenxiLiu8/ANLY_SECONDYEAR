###### Data Cleaning for US_Dataset_PowerPlants_Locations_Nature_County.csv
import pandas as pd
import numpy as np
import reverse_geocoder as rg





df = pd.read_csv("US_Dataset_PowerPlants_Locations_Nature_County.csv")

df.dtypes
####  fix the float year
int_year = []
error = []
for i in range(len(df)):
    try:
        int_year.append(int(df['commissioning_year'][i]))
    except:
        error.append(i)
        int_year.append(0)


### Notice those row that have empty years are in have differnt identifer WRI instead of USA


df['commissioning_year'] = int_year



#####Match the lat and long to the county and state using reverse geocoder package
state = []
county = []
for i in range(len(df)):
    result = rg.search((df['latitude'][i],df['longitude'][i]))
    state.append(result[0]['admin1'])
    county.append(result[0]['admin2'])


len(state)
len(county)

df['state'] = state
df['county'] = county


df.to_csv("power_plants_cleaned.csv",index=False)