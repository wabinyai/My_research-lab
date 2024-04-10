from datetime import datetime, timedelta
import datetime as dt
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import numpy as np
import os
import random
import string
import ee
from functools import reduce
import geemap 
from pymongo import MongoClient
from bson.json_util import dumps
from pymongo import MongoClient

from configure import Config

credentials = ee.ServiceAccountCredentials(
    key_file=Config.GOOGLE_APPLICATION_CREDENTIALS,
    email=Config.GOOGLE_APPLICATION_CREDENTIALS_EMAIL,
)
class DataHandler:
    def __init__(self):
        self.client = bigquery.Client()
        self.data_path = None
        ee.Initialize(credentials, project=Config.GOOGLE_PROJECT_ID)
        self.mongo_client = MongoClient(Config.MONGODB_URI)
        self.db = self.mongo_client[Config.MONGODB_DATABASE]
        self.collection = self.db[Config.MONGODB_COLLECTION]

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
                pm10, country
            FROM {Config.BIGQUERY_HOURLY_CONSOLIDATED}
            WHERE timestamp BETWEEN TIMESTAMP('{start_time.isoformat()}')
                AND TIMESTAMP('{end_time.isoformat()}')
                AND pm2_5 IS NOT NULL
                AND site_latitude IS NOT NULL
            LIMIT 500;
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
        site_geolocation = query_bigquery[['site_name', 'site_id', 'site_latitude', 'site_longitude',  'country']]
        geo_df = site_geolocation.groupby(['site_id']).agg({
            'site_name': 'first',
            'site_latitude': 'first',
            'site_longitude': 'first',
            'country': 'first'
        }).reset_index()
        
        return geo_df
    
    def get_data_df(self, df, geo_df):
        site_names = {}
        for site_id in df.site_id.unique():
            site_names[site_id] = df[df.site_id == site_id].site_name.mode()[0]

        site_df = pd.DataFrame(columns=['site_id', 'site_name', 'site_latitude', 'site_longitude', 'start_date','end_date','country'])

    def get_site_names(self, df):
        site_names = {}
        for site_id in df.site_id.unique():
            site_names[site_id] = df[df.site_id == site_id].site_name.mode()[0]
        return site_names
    
    def get_site_df(self, df):
      site_df = pd.DataFrame(columns=['site_id', 'site_latitude', 'site_longitude', 'start_date', 'end_date', 'country'])
      for i in df.site_id.unique():
          dff = df[df.site_id == i].reset_index(drop=True)
          start_date = dff.timestamp.min()
          end_date = dff.timestamp.max()
          site_latitude = dff.site_latitude.mode()[0]
          site_longitude = dff.site_longitude.mode()[0]
          country = dff.country.mode()[0]
          row = [i, site_latitude, site_longitude, start_date, end_date,  country]
          site_df = pd.concat([site_df, pd.DataFrame([row], columns=site_df.columns)], ignore_index=True)

      site_df.start_date = pd.to_datetime(site_df.start_date)
      site_df.end_date = pd.to_datetime(site_df.end_date)

      return site_df
    
    def ee_array_to_df(self, arr, list_of_bands):
        df = pd.DataFrame(arr)
        headers = df.iloc[0]
        df = pd.DataFrame(df.values[1:], columns=headers)
        df = df[['longitude', 'latitude', 'time', *list_of_bands]].dropna()
        for band in list_of_bands:
            df[band] = pd.to_numeric(df[band], errors='coerce')
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')
        df = df[['datetime', *list_of_bands]]
        return df
    
    def satellite_image(self):
        images = {
            'Offline_UV_Aerosol_Index': 'COPERNICUS/S5P/OFFL/L3_AER_AI',
            'SulphurDioxide': 'COPERNICUS/S5P/NRTI/L3_SO2',
            'CarbonMonoxide': 'COPERNICUS/S5P/NRTI/L3_CO',
            'NitrogenDioxide': 'COPERNICUS/S5P/NRTI/L3_NO2',
            'Formaldehyde': 'COPERNICUS/S5P/NRTI/L3_HCHO',
            'UvAerosolIndex': 'COPERNICUS/S5P/NRTI/L3_AER_AI',
            'Ozone': 'COPERNICUS/S5P/NRTI/L3_O3',
            
  
        }
        return images
    
    def get_image_data(self, site_df):
        dfs = {}
        images = self.satellite_image()
        for product, image in images.items():
            site_dfs = {}
            for i in site_df.itertuples():
                site, latitude, longitude = i.site_id, i.site_latitude, i.site_longitude
                start_date = str(i.start_date.date() - dt.timedelta(days=1))
                end_date = str(i.end_date.date() + dt.timedelta(days=1))
                site_location = ee.Geometry.Point(longitude, latitude)

                image_collection = ee.ImageCollection(image)
                if image_collection.size().getInfo() == 0:
                    print(f"No images available for {product}. Skipping.")
                    continue

                band_names = image_collection.first().bandNames().getInfo()

                # Selection of appropriate bands and dates.
                selected_bands = image_collection.select(ee.List(band_names)).filterDate(start_date, end_date)
                if selected_bands.size().getInfo() == 0:
                    print(f"No images available for {product} within the specified date range. Skipping.")
                    continue

                data = selected_bands.getRegion(site_location, 10).getInfo()
                data_df = self.ee_array_to_df(data, band_names)
                data_df.columns = [product + '_' + x for x in data_df.columns]
                data_df['date'] = data_df[product + '_' + 'datetime'].map(lambda x: x.strftime('%Y-%m-%d'))
                data_df['month'] = data_df[product + '_' + 'datetime'].dt.month
                data_df['hour'] = data_df[product + '_' + 'datetime'].dt.hour
                site_dfs[site] = data_df

            dfs[product] = site_dfs

        return dfs

    def process_site_data(self, dfs):

        site_dfs = {}
        try:
            for site in dfs[list(dfs.keys())[0]].keys():
                products = []
                # Iterate over each product
                for product, site_df in dfs.items():
                    # Retrieve dataframe for the current product and site
                    product_df = site_df[site]
                    product_df = product_df.groupby(['date', 'hour']).mean().reset_index()
                    products.append(product_df)

                # Merge dataframes for all products
                merged_df = reduce(lambda left, right: pd.merge(left, right, on=['date', 'hour','month'], how='outer'), products)
                merged_df['site_id'] = site
                site_dfs[site] = merged_df

        except Exception as e:
            print(f"Error processing site data: {e}")

        return site_dfs
    

    def merge_site_data(self, site_dfs):
        result_df = pd.DataFrame()
        for key in site_dfs.keys():
          result_df = pd.concat([result_df, site_dfs[key]])
        return result_df
    
    def extract_and_merge_data(self, df, result_df):
      df1 = df[['site_id', 'site_name', 'pm2_5', 'pm10', 'date', 'site_latitude', 'site_longitude', 'country', 'month', 'hour']]
      merged_df_ = df1.merge(result_df, how='right', on=['site_id', 'date', 'month', 'hour'])
      merged_df_= merged_df_[~merged_df_['country'].isna()].reset_index(drop = True)
      merged_df_ = merged_df_.drop(columns=[col for col in merged_df_.columns if '_datetime' in col])
      merged_df_.to_csv('output.csv', index=False)

      return merged_df_
    
    def save_to_mongodb(self, merged_df_):
        try:
            for record in merged_df_.to_dict(orient='records'):
                # Check if the record already exists in the database
                existing_record = self.collection.find_one({
                    'site_id': record['site_id'],
                    'date': record['date'],
                    'hour': record['hour'],
                    'pm2_5': record['pm2_5'],
                })
                if existing_record:
                    # Update existing record with new data
                    new_data = {key: value for key, value in record.items() if key not in ['site_id', 'date', 'hour']}
                    self.collection.update_one(
                        {'_id': existing_record['_id']},
                        {'$set': new_data}
                    )
                else:
                    # Insert new record
                    self.collection.insert_one(record)
            print("Data saved to MongoDB successfully.")
        except Exception as e:
            print(f"Error saving data to MongoDB: {e}")