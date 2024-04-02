import mysql.connector
import yaml
from profilehooks import timecall

@timecall
def load_data():
    # read the config file
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    # database configuration
    db_config = config['database']

    # establish a database connection using the varibles from the config file
    conn = mysql.connector.connect(**db_config)

    # inserting data into the table restaurants
    cursor = conn.cursor()
    
    # read the data
    csv_file = "data_cleaned/restaurants_cleaned.csv"
    
    # construct the sql statement to load data from the csv file
    load_data_query = f"LOAD DATA INFILE '{csv_file}' INTO TABLE restaurants FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES"
    
    # execute the statement
    cursor.execute(load_data_query)