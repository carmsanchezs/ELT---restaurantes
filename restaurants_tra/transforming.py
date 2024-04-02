#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from profilehooks import timecall


def set_category(price):
    """Set a price category depends of the characters in price"""
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


@timecall
def transform_data():
    """Change the necesary data, like location, price, cuisine, etc.
       based in business rules."""
    # read data
    restaurants = pd.read_csv('ods/michelin_my_maps.csv',
                              index_col=0,
                              dtype={'PhoneNumber': str})

    # filtering by Award: 1 Star, 2 Stars, 3 Stars
    restaurants = restaurants[restaurants.Award.isin(
        ['3 Stars', '2 Stars', '1 Star']
    )]

    # split Location and Country
    restaurants[['Location2',
                'Country']] = restaurants.Location.str.split(',', expand=True)

    # categorize Price
    restaurants['Price'] = restaurants.Price.str.replace(
        '[¥€£₩฿₺₫]',
        '$',
        regex=True
    )

    restaurants['PriceCategory'] = restaurants.Price.apply(set_category)

    # spit Cuisine
    restaurants[['Cuisine1', 'Cuisine2']] = restaurants.Cuisine.str.replace(
            '/', ','
        ).str.split(
            ',', expand=True
        )

    # Working with "FacilitiesAndServices" to divide it into a maximun of 5 columns
    restaurants[
        ['FacilitiesAndServices1',
        'FacilitiesAndServices2',
        'FacilitiesAndServices3',
        'FacilitiesAndServices4',
        'FacilitiesAndServices5']] = restaurants.FacilitiesAndServices.str.split(
            ',', expand=True
        ).iloc[:, :5]

    # Remove invalid telephone numbers or nulls
    # only keep the number grather than 10 and lower than 13
    restaurants = restaurants[(restaurants.PhoneNumber.str.len() >= 10) & (restaurants.PhoneNumber.str.len() <= 13)]

    # Adding a field to restaurants with music in the description
    restaurants['Music'] = np.where(restaurants.Description.str.contains('music'), 'Yes', 'No')
    
    # Save the cleaned data to a CSV file
    # drop columns
    restaurants.drop(['Location', 'Price', 'Cuisine', 'FacilitiesAndServices'],
                     axis=1,
                     inplace=True)

    # redefining columns
    cols = ['Name', 'Address', 'Longitude',
        'Latitude', 'PhoneNumber', 'Url', 'WebsiteUrl', 'Award', 'Description',
        'Location', 'Country',
        'Price', 'Cuisine1', 'Cuisine2', 'FacilitiesAndServices1',
        'FacilitiesAndServices2', 'FacilitiesAndServices3',
        'FacilitiesAndServices4', 'FacilitiesAndServices5', 'Music']

    restaurants.columns = cols
    restaurants.index.names = ['id']
    restaurants.to_csv('./data_cleaned/restaurants_cleaned.csv')
    print('Data transformation done.')
