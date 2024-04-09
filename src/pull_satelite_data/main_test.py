from utils import DataHandler
from datetime import datetime, timedelta
import time

def main():
    # Create an instance of DataHandler
    data_handler = DataHandler()

    # Example usage of query_bigquery_batch
    start_time = datetime.now() - timedelta(days=26)
    end_time = datetime.now()
    batch_size = 5000
    total_rows = 0

    while True:
        print("Querying BigQuery...")
        data = data_handler.query_bigquery_batch(start_time=start_time, end_time=end_time, batch_size=batch_size)
        if data.empty:
            break
        print("Querying BigQuery complete.")

        print("Processing geolocation data...")
        geo_data = data_handler.site_geolocation_data(data)
        site_names = data_handler.get_site_names(data)
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
        data_handler.save_to_mongodb(merged_df_)
        print("Merged data saved to MongoDB.")

        total_rows += len(data)
        print(f"Processed {total_rows} rows.")

        # Pause for 5 minutes before next batch
        time.sleep(300)

if __name__ == "__main__":
    main()