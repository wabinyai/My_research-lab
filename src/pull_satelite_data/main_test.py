from utils import DataHandler
from datetime import datetime, timedelta

def main():
    # Create an instance of DataHandler
    data_handler = DataHandler()

    # Example usage of query_bigquery
    start_time = datetime.now() - timedelta(days=26)
    end_time = datetime.now()
    print("Querying BigQuery...")
    data = data_handler.query_bigquery(start_time=start_time, end_time=end_time)
    print("Querying BigQuery complete.")

    print("Processing geolocation data...")
    geo_data = data_handler.site_geolocation_data(data)
    print("Geolocation data processed.")

    print("Getting site names...")
    site_names = data_handler.get_site_names(data)
    print("Site names retrieved.")

    print("Creating site dataframe...")
    site_df = data_handler.get_site_df(data)
    print("Site dataframe created.")

    print("Getting image data for sites...")
    dfs = data_handler.get_image_data(site_df)
    print("Image data retrieved.")

    print("Processing site data...")
    site_dfs = data_handler.process_site_data(dfs)
    print("Site data processed.")

    print("Merging site data...")
    all_data_dfs = data_handler.merge_site_data(site_dfs)
    print("Site data merged.")

    print("Extracting and merging data...")
    merged_df_ = data_handler.extract_and_merge_data(data, all_data_dfs)
    print("Data extraction and merging complete.")
    
    print("Saving merged data to MongoDB...")
    data_handler.save_to_mongodb(merged_df_)
    print("Merged data saved to MongoDB.")
    
    print(merged_df_)

if __name__ == "__main__":
    main()
