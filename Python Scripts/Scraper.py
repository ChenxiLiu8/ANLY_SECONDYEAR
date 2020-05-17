#### Web scriper for https://www.epa.gov/superfund/national-priorities-list-npl-sites-state Data
import requests
from bs4 import BeautifulSoup 
import pandas as pd 
import re 
import numpy as np
from pandas import Series, DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen as uReq
import bs4

##### Make the request 
#my_url = 'https://www.epa.gov/superfund/national-priorities-list-npl-sites-state#main-content'
#driver = webdriver.Chrome()
#driver.set_window_size(1120,550)
#driver.implicitly_wait(10)
#driver.get(my_url)
#table_list = driver.find_elements(By.TAG_NAME,"td")
#count = 0
#site_name = []
#city = []
#site_id = []
#list_date = []
#site_score = []
#indicator = []



##### Read in the data as list 
#for table in table_list:
#    if count == 0:
#       site_name.append(table.text)
 #       count += 1 
  #  elif count == 1:
   #     city.append(table.text)
    #    count += 1 
#    elif count == 2:
#        site_id.append(table.text)
#        count += 1 
 #   elif count == 3:
 #       list_date.append(table.text)
 #       count += 1 
  #  elif count == 4:
   #     site_score.append(table.text)
    #    count += 1 
   # elif count == 5:
    #    indicator.append(table.text)
     #   count += 1 
  #  elif count == 7:
   #     count = 0
    #else: 
     #   count += 1
        


####### Scrape FIP
fips = []
names = []
states = []

fip_url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013697'
page = uReq(fip_url, timeout=5)
page_html = page.read()
page.close()

    
soup = BeautifulSoup(page_html, "html.parser")        

containers = soup.find("table",{"class":"data"})
for tr in containers.children:
    if isinstance(tr,bs4.element.Tag):
        tds = tr('td')
        n = 0
        m = 1
        k = 2
        while n < len(tds) and m < len(tds) and k < len(tds):
            fips.append(tds[n].string)
            names.append(tds[m].string)
            states.append(tds[k].string)
            n += 3
            m += 3
            k += 3




            
df = pd.DataFrame(list(zip(fips,names,states)),columns = ['fips','names','states'])  

df.to_csv("FIPS_Info.csv",index = False)