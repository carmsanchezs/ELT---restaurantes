import pandas as pd
from profilehooks import timecall


@timecall
def extract_data():
    df = pd.read_csv('../data/michelin_my_maps.csv', dtype={'PhoneNumber': str})
    df.to_csv('ods/michelin_my_maps.csv')
    print("Data extraction done.")
