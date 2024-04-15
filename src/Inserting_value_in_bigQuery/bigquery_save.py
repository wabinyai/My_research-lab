import os
from datetime import datetime
from tqdm import tqdm  # Import tqdm library for progress bar

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from config import Config

def column_mapping(file):
    data = pd.read_csv(file)
    renaming = {'device_latitude': 'latitude',
                'device_longitude': 'longitude',
                'device_name': 'device_id',
                's1_pm2_5': 's1_pm2_5',
                'pm2_5': 'pm2_5',
                # 's2_pm2_5': 's2_pm2_5',
                'datetime': 'timestamp',
                'tenant': 'tenant',
               # 'site_id': 'site_id',
                # 'site_name': ,
                # 'site_latitude': 'latitude',
                # 'site_longitude': 'longitude',
                # 'device_name_1': '',
                # 'frequency': 
                }
    data.rename(columns = renaming, inplace=True)
    data['s1_pm2_5'] = pd.to_numeric(data['s1_pm2_5'], errors='coerce')
    
    # Parse and reformat 'timestamp' column
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data_sub = data[['tenant', 'timestamp', 'site_id', 'device_id', 'latitude', 'longitude', 'pm2_5']]
    data_sub.fillna('', inplace=True)

    return data_sub

def save_predictions_on_bigquery(file):
    data = column_mapping(file)
    data_json = data.to_dict(orient='records')

    client = bigquery.Client()

    # Calculate the total number of rows for the progress bar
    total_rows = len(data_json)
    
    with tqdm(total=total_rows, desc="Inserting rows to BigQuery....") as pbar:
        # Iterate through data_json and insert rows
        for chunk in chunks(data_json, chunk_size=1000):  # Adjust chunk size as per your requirement
            errors = client.insert_rows_json( 
             #   json_rows=chunk, table=Config.BIGQUERY_DEVICE_MEASUREMENT_STAGE, skip_invalid_rows=True
                json_rows=chunk, table=Config.BIGQUERY_DEVICE_MEASUREMENT_PROD, skip_invalid_rows=True
            )
            if errors:
                print("Encountered errors while inserting rows:", errors)
            else:
                pbar.update(len(chunk))  # Update progress bar with the number of rows inserted
        print("Data inserted successfully!")

def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size] 

if __name__ == "__main__":
    file = 'D:/AIRQO/data/ArbaMinch_AirQo_files/sp12.csv'
    save_predictions_on_bigquery(file=file)
