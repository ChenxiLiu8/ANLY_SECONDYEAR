import pandas as pd 
import numpy as np 

df_pp = pd.read_csv("Power_Plants_FINAL.csv")
df_pp.dtypes

set(df_pp['primary_fuel'])

df_bio = df_pp.loc[df_pp['primary_fuel']=='Biomass']
df_coal =df_pp.loc[df_pp['primary_fuel']=='Coal']
df_cogen=df_pp.loc[df_pp['primary_fuel']=='Cogeneration']
df_gas=df_pp.loc[df_pp['primary_fuel']=='Gas']
df_geo=df_pp.loc[df_pp['primary_fuel']=='Geothermal']
df_hydro=df_pp.loc[df_pp['primary_fuel']=='Hydro']
df_nuclear=df_pp.loc[df_pp['primary_fuel']=='Nuclear']
df_oil=df_pp.loc[df_pp['primary_fuel']=='Oil']
df_petcoke=df_pp.loc[df_pp['primary_fuel']=='Petcoke']
df_solar=df_pp.loc[df_pp['primary_fuel']=='Solar']
df_storage =df_pp.loc[df_pp['primary_fuel']=='Storage']
df_waste=df_pp.loc[df_pp['primary_fuel']=='Waste']
df_wind=df_pp.loc[df_pp['primary_fuel']=='Wind']

len(df_bio)
len(df_coal)
len(df_cogen)
len(df_gas)
len(df_geo)
len(df_hydro)
len(df_nuclear)
len(df_oil)
len(df_petcoke)
len(df_solar)
len(df_waste)
len(df_wind)


output = ['name','latitude','longitude','primary_fuel','state','normalized_county','Fips']

df_bio.to_csv("app_biomass.csv",index=False,columns = output)
df_coal.to_csv("app_coal.csv",index=False,columns = output)
df_cogen.to_csv("app_cogen.csv",index=False,columns = output)
df_gas.to_csv("app_gas.csv",index=False,columns = output)
df_geo.to_csv("app_geo.csv",index=False,columns = output)
df_hydro.to_csv("app_hydro.csv",index=False,columns = output)
df_nuclear.to_csv("app_nuclear.csv",index=False,columns = output)
df_petcoke.to_csv("app_petcoke.csv",index=False,columns = output)
df_solar.to_csv("app_solar.csv",index=False,columns = output)
df_waste.to_csv("app_waste.csv",index=False,columns = output)
df_wind.to_csv("app_wind.csv",index=False,columns = output)
df_oil.to_csv("app_oil.csv",index=False,columns = output)