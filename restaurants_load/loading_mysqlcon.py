import mysql.connector
import pandas as pd
import yaml


def load_data():
    # read the config file
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    # database configuration
    db_config = config['database']

    # establish a database connection using the varibles from the config file
    conn = mysql.connector.connect(**db_config)

    # read the data
    restaurants = pd.read_csv(r"data_cleaned/restaurants_cleaned.csv",
                              index_col=0)

    # inserting data into the table restaurants
    cursor = conn.cursor()
    insert_query = """INSERT INTO restaurants(
            id,
            Name,
            Address,
            Longitude,
            Latitude,
            PhoneNumber,
            Url,
            WebsiteUrl,
            Award,
            Description,
            Location,
            Country,
            Price,
            Cuisine1,
            Cuisine2,
            FacilitiesAndServices1,
            FacilitiesAndServices2,
            FacilitiesAndServices3,
            FacilitiesAndServices4,
            FacilitiesAndServices5)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    for id, row in restaurants.iterrows():
        cursor.execute( insert_query, (
                        id,
                        row.Name,
                        row.Address,
                        row.Longitude,
                        row.Latitude,
                        row.PhoneNumber,
                        row.Url,
                        row.WebsiteUrl,
                        row.Award,
                        row.Description,
                        row.Location,
                        row.Country,
                        row.Price,
                        row.Cuisine1,
                        row.Cuisine2,
                        row.FacilitiesAndServices1,
                        row.FacilitiesAndServices2,
                        row.FacilitiesAndServices3,
                        row.FacilitiesAndServices4,
                        row.FacilitiesAndServices5))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data loading done.")
