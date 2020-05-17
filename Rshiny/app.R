
#### import packages
library(leaflet)
library(sp)
library(mapproj)
#library(maps)
library(mapdata)
library(maptools)
library(htmlwidgets)
library(magrittr)
library(XML)
library(plyr)
library(rgdal)
library(WDI)
library(raster)
library(stringr)
library(tidyr)
library(tigris)
library(rgeos)
library(ggplot2)
library(scales)
library(shiny)
library(rsconnect)

#### Readin data
CancerRates <- read.csv('Cancer_Rate_FINAL.csv')
NPL_Site <- read.csv('NPL_Site_FINAL.csv')
bio_plants <- read.csv('app_biomass.csv')
coal_plants <- read.csv('app_coal.csv')
nuclear_plants <- read.csv('app_nuclear.csv')
gas_plants <- read.csv('app_gas.csv')
oil_plants <- read.csv('app_oil.csv')
petcoke_plants <- read.csv('app_petcoke.csv')


#### change cancer rate colnames to lower
names(CancerRates) <- tolower(names(CancerRates))
####### change the cancer rate colnames
colnames(CancerRates) <- c("State", "GEOID", "Average.Annual.Count",'Recent.Trend','incidence.rate.trend','county','State.Code','Cancer.Rate')
#####fill in the geoid (5-digits string)

CancerRates$GEOID <- formatC(CancerRates$GEOID, width = 5, format = "d", flag = "0")

#### load in the shape file
us.map <- readOGR(dsn = ".", layer = "cb_2018_us_county_20m", stringsAsFactors = FALSE)

##### remove outside islands from the shapefile

us.map <- us.map[!us.map$STATEFP %in% c("15", "72", "66", "78", "60", "69",
                                        "64", "68", "70", "74"),]
us.map <- us.map[!us.map$STATEFP %in% c("81", "84", "86", "87", "89", "71", "76",
                                        "95", "79"),]
##### merge the map with cancer rate data
cancermap <- merge(us.map, CancerRates, by=c("GEOID"))

##### edit pop out to the cancer rate heat map

popup_dat <- paste0("<strong>County: </strong>", 
                    cancermap$county, 
                    "<br><strong>Cancer Rate (Age Adjusted): </strong>", 
                    cancermap$Cancer.Rate)

#### edit pop out to the NPL Site marker
popup_LU <- paste0("<strong>Use Name: </strong>", 
                   NPL_Site$Site.Name, 
                   "<br><strong>Score: </strong>", 
                   NPL_Site$Site.Score)
popup_bio <- paste0("<strong>Use Name: </strong>", 
                    bio_plants$name, 
                     "<br><strong>Primary Fuel: </strong>", 
                    bio_plants$primary_fuel,
                     "<br><strong>State: </strong>",
                    bio_plants$state,
                     "<br><strong>County: </strong>",
                    bio_plants$normalized_county)

popup_coal <- paste0("<strong>Use Name: </strong>", 
                    coal_plants$name, 
                   "<br><strong>Primary Fuel: </strong>", 
                   coal_plants$primary_fuel,
                   "<br><strong>State: </strong>",
                   coal_plants$state,
                   "<br><strong>County: </strong>",
                   coal_plants$normalized_county)

popup_nuclear <- paste0("<strong>Use Name: </strong>", 
                    nuclear_plants$name, 
                    "<br><strong>Primary Fuel: </strong>", 
                    nuclear_plants$primary_fuel,
                    "<br><strong>State: </strong>",
                    nuclear_plants$state,
                    "<br><strong>County: </strong>",
                    nuclear_plants$normalized_county)

popup_gas <- paste0("<strong>Use Name: </strong>", 
                    gas_plants$name, 
                    "<br><strong>Primary Fuel: </strong>", 
                    gas_plants$primary_fuel,
                    "<br><strong>State: </strong>",
                    gas_plants$state,
                    "<br><strong>County: </strong>",
                    gas_plants$normalized_county)

popup_oil <- paste0("<strong>Use Name: </strong>", 
                    oil_plants$name, 
                    "<br><strong>Primary Fuel: </strong>", 
                    oil_plants$primary_fuel,
                    "<br><strong>State: </strong>",
                    oil_plants$state,
                    "<br><strong>County: </strong>",
                    oil_plants$normalized_county)

popup_petcoke <- paste0("<strong>Use Name: </strong>", 
                    petcoke_plants$name, 
                    "<br><strong>Primary Fuel: </strong>", 
                    petcoke_plants$primary_fuel,
                    "<br><strong>State: </strong>",
                    petcoke_plants$state,
                    "<br><strong>County: </strong>",
                    petcoke_plants$normalized_county)

pal <- colorQuantile("YlOrRd", NULL, n = 9)

##### make icons 
npl_icon = makeIcon("npl_icon.png","npl_icon.png",24,24)
nuclear_icon = makeIcon("nuclear_icon.png","nuclear_icon.png",24,24)
coal_icon = makeIcon("coal_icon.png","coal_icon.png",24,24)
bio_icon = makeIcon("bio_icon.png","bio_icon.png",24,24)
gas_icon = makeIcon("gas_icon.png","gas_icon.png",24,24)
oil_icon = makeIcon("oil_icon.png","oil_icon.png",24,24)
# Define UI for application that draws a histogram
ui <- shinyUI(bootstrapPage(
        leafletOutput("gmap",height = "500")
    )
)


# Define server logic required to draw a histogram
server <- function(input, output) {

    output$gmap <- renderLeaflet({
        leaflet(data = cancermap) %>%
            # Base groups
            addTiles() %>%
            setView(lng = -93, lat = 40, zoom = 4) %>% 
            addPolygons(fillColor = ~pal(Cancer.Rate), 
                        fillOpacity = 0.8, 
                        color = "#BDBDC3", 
                        weight = 1,
                        popup = popup_dat,
                        group="Cancer Rate by Counties") %>% 
            # Overlay groups
            addMarkers(data=NPL_Site,lat=~Latitude, lng=~Longitude, popup=popup_LU, icon = npl_icon,group = "NPL Sites") %>% 
            addMarkers(data=bio_plants,lat=~latitude, lng=~longitude, popup=popup_bio, icon = bio_icon, group = "Biomass Power Plants") %>% 
            addMarkers(data=coal_plants,lat=~latitude, lng=~longitude, popup=popup_coal, icon = coal_icon, group = "Coal Power Plants" ) %>% 
            addMarkers(data=nuclear_plants,lat=~latitude, lng=~longitude, popup=popup_nuclear,icon = nuclear_icon, group = "Nuclear Power Plants") %>% 
            addMarkers(data=gas_plants,lat=~latitude, lng=~longitude, popup=popup_gas, icon = gas_icon, group = "Gas Power Plants") %>% 
            addMarkers(data=oil_plants,lat=~latitude, lng=~longitude, popup=popup_oil, icon = oil_icon, group = "Oil Power Plants") %>% 
            #addMarkers(data=petcoke_plants,lat=~latitude, lng=~longitude, popup=popup_petcoke, group = "Petcoke Power Plants") %>% 
            #addCircles(~long, ~lat, ~10^lag/5, stroke = F, group = "Quakes") %>%
            #addPolygons(data = outline, lng = ~long, lat = ~lat,
            #           fill = F, weight = 2, color = "#FFFFCC", group = "Outline") %>%
            # Layers control
            
            addLayersControl(
                baseGroups = c("Cancer Rate by Counties"),
                overlayGroups = c("NPL Sites","Biomass Power Plants","Coal Power Plants","Nuclear Power Plants","Gas Power Plants","Oil Power Plants"),
                #overlayGroups = c("PowerPlants Site"),
                options = layersControlOptions(collapsed = FALSE)
            ) %>%
            hideGroup("NPL Sites")%>%
            hideGroup("Biomass Power Plants")%>%
            hideGroup("Coal Power Plant")%>%
            hideGroup("Nuclear Power Plants")%>%
            hideGroup("Gas Power Plants")%>%
            hideGroup("Oil Power Plants")%>%
            hideGroup("Coal Power Plants")
            
                
            
        
    })
}

# Run the application 
shinyApp(ui = ui, server = server)

