# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 15:23:13 2016

@author: Doug
"""

#import libraries
import urllib2
import json
import pandas as pd

#define the addresses to put through the loop
#these are just 2 hard coded examples from 2 different cities 
#but this list could come from a separate csv or from a scraped list of favorited zillow homes
homes = [\
  '920 S State St, Raleigh, NC, 27601',\
  '2216 E Marshall St, Richmond, VA, 23223'
]

print homes

#create empty data frame with 9 column headers
#this is where the values from the API will go
homes_codes= pd.DataFrame(columns=['city', 'county', 'state','tract', 'block' ,
                'blockgroup', 'county_geo_id', 'tract_geo_id', 'block_geo_id'])

#call the api url and read json
#loop over  url + 'address(i)' + rest of url
for i in homes:
    f = urllib2.urlopen('https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=' +
                        i + 
                        '&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layers=14&format=json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    #Assign variables to parsed json values, one variable for each column
    # 9 variables total that we want to grab 
    # all of these are census ids that will be useful for calling other census apis
    city = parsed_json['result']['addressMatches'][0]['addressComponents']['city']
    county = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['COUNTY']
    state = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['STATE']
    tract = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']
    block = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['BLOCK']
    blockgroup = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['BLKGRP']
    county_geo_id = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['COUNTY']
    tract_geo_id = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']
    block_geo_id = parsed_json['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['GEOID']
   
    #within the for loop, write to the ith row of the data frame
    #Use df.ix[i] to "locate" the ith row and write the pandas series to it
    #NOTE: This creates an index int he first column with address values
    homes_codes.ix[i] = pd.Series({'city':city, 'county':county, 'state':state ,'tract':tract,
    'block':block, 'blockgroup':blockgroup, 'county_geo_id':county_geo_id,
    'tract_geo_id':tract_geo_id, 'block_geo_id':block_geo_id})
  
#closing the url call
f.close()  

#checking to see if it correctly called the API and wrote rows to the data frame
print homes_codes

#write the dataframe to csv 
#address will show up in the first column as an index            
homes_codes.to_csv('homes_codes.csv')



