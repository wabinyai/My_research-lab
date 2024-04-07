from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import numpy as np
import os
import random
import string
import ee
from configure import Config

credentials = ee.ServiceAccountCredentials(
    key_file=Config.GOOGLE_APPLICATION_CREDENTIALS,
    email=Config.GOOGLE_APPLICATION_CREDENTIALS_EMAIL,
)
ee.Initialize(credentials)

class DataHandler:
    def __init__(self):
        self.client = bigquery.Client()
        self.data_path = None

    SEED = 89561

    def seeder(self, seed):
        random.seed(seed)
        np.random.default_rng(seed)
        np.random.seed(seed)

    def random_id(self, N=10):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))
    
    def query_bigquery(self, start_time=None, end_time=None):
        if not start_time:
            start_time = datetime.now() - timedelta(days=7)
        if not end_time:
            end_time = datetime.now()

        query = f"""
            SELECT 
                site_id, timestamp, site_name, site_latitude, site_longitude, pm2_5,
                pm10, country, region, city, county
            FROM {Config.BIGQUERY_HOURLY_CONSOLIDATED}
            WHERE timestamp BETWEEN TIMESTAMP('{start_time.isoformat()}')
            AND TIMESTAMP('{end_time.isoformat()}')
            AND pm2_5 IS NOT NULL
            AND site_latitude IS NOT NULL
        """

        try:
            query_job = self.client.query(query)
            df = query_job.to_dataframe() 
            df = df.sort_values(by=['site_name', 'timestamp']).reset_index(drop=True)
            df['date'] = [str(x.date()) for x in df.timestamp]
            df['month'] = df.timestamp.dt.month
            df['hour'] = df.timestamp.dt.hour
            return df
        except Exception as e:
            print(f"Error querying BigQuery: {e}")
            return None
        
    def site_geolocation_data(self, query_bigquery):
        site_geolocation = query_bigquery[['site_name', 'site_id', 'site_latitude', 'site_longitude', 'city', 'country']]
        geo_df = site_geolocation.groupby(['site_id']).agg({
            'site_name': 'first',
            'site_latitude': 'first',
            'site_longitude': 'first',
            'city': 'first',
            'country': 'first'
        }).reset_index()
        
        return geo_df
