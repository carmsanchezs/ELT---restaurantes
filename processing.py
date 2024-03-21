from restaurants_ext.extracting import extract_data
from restaurants_tra.transforming import transform_data
from restaurants_load.loading_mysqlcon import load_data

extract_data()
transform_data()
load_data()
