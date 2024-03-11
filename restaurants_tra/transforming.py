#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re

# read data
original_df = pd.read_csv('../ods/michelin_my_maps.csv', 
                          dtype={'PhoneNumber': str}
                          )

# make a copy of the original data frame
restaurants_df = original_df.copy(deep=True)

# set an index
restaurants_df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
restaurants_df.set_index('id', inplace=True)

# ### Location2 and country
restaurants_df[['Location2', 'Country']] = restaurants_df.Location.apply(
    lambda s: pd.Series(s.strip().split(","))
    )

# ### price
# replace in order to have only $ 
pattern = re.compile('[¥€£₩฿₺₫]')
restaurants_df['Price'] = restaurants_df.Price.apply(
    lambda s: pd.Series(pattern.sub('$', str(s)))
    )


def set_category(price):
    if price == '$':
        return 'Muy Barato'
    elif price == '$$':
        return 'Accesible'
    elif price == '$$$':
        return 'Normal'
    elif price == '$$$$':
        return 'Costoso'
    elif price == '$$$$$':
        return 'Muy Costoso'
    else:
        return None


restaurants_df['PriceCategory'] = restaurants_df.Price.apply(set_category)


# ### Cuisine
# replacing / by ,
restaurants_df['Cuisine'] = restaurants_df.Cuisine.apply(
    lambda s: pd.Series(s.replace('/', ','))
    )
# split the value of Cuisene
restaurants_df[['Cuisine1', 'Cuisine2']] = restaurants_df.Cuisine.apply(
    lambda s: pd.Series(s.strip().split(','))
    )


# ### Filtering by 'Award': 1 Start, 2 Starts, 3 Starts

restaurants_123 = restaurants_df[restaurants_df.Award.isin(
        ['3 Stars', '2 Stars', '1 Star']
    )]


# ### Working with "FacilitiesAndServices" to divide it into 
# a maximun of five columns
restaurants_123[
    ['FacilitiesAndServices1', 
     'FacilitiesAndServices2', 
     'FacilitiesAndServices3', 
     'FacilitiesAndServices4', 
     'FacilitiesAndServices5']] = restaurants_123.FacilitiesAndServices.apply(
         lambda s: pd.Series(str(s).strip().split(',')).iloc[:5]
         )


# save the cleaned data to a CSV file
restaurants_cleaned = restaurants_123[['Name', 'Address', 'Longitude',
       'Latitude', 'PhoneNumber', 'Url', 'WebsiteUrl', 'Award', 'Description',
       'Location2', 'Country',
       'PriceCategory', 'Cuisine1', 'Cuisine2', 'FacilitiesAndServices1',
       'FacilitiesAndServices2', 'FacilitiesAndServices3',
       'FacilitiesAndServices4', 'FacilitiesAndServices5']]
cols = ['Name', 'Address', 'Longitude',
       'Latitude', 'PhoneNumber', 'Url', 'WebsiteUrl', 'Award', 'Description',
       'Location', 'Country',
       'Price', 'Cuisine1', 'Cuisine2', 'FacilitiesAndServices1',
       'FacilitiesAndServices2', 'FacilitiesAndServices3',
       'FacilitiesAndServices4', 'FacilitiesAndServices5']
restaurants_cleaned.columns = cols
restaurants_cleaned.to_csv('../data_cleaned/restaurants_cleaned.csv')
