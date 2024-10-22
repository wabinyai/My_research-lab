from utils import DataHandler
from datetime import datetime, timedelta
import time

def main():
    # Create an instance of DataHandler
    data_handler = DataHandler()

    # Example usage of query_bigquery
    start_time = datetime.now() - timedelta(days=26)
    end_time = datetime.now()
    data = data_handler.query_bigquery(start_time=start_time, end_time=end_time)
    geo_data = data_handler.site_geolocation_data(data)
    site_names = data_handler.get_site_names(data)
    site_df = data_handler.get_site_df(data) 
    dfs = data_handler.get_image_data(site_df)
    site_dfs = data_handler.process_site_data(dfs)
    all_data_dfs = data_handler.merge_site_data(site_dfs)
    merged_df_ = data_handler.extract_and_merge_data(data, all_data_dfs)
    data_handler.save_to_mongodb(merged_df_)
    print("Merged data saved to MongoDB.")
    print(merged_df_)
 
if __name__ == "__main__":
    main()
