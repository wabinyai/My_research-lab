from utils import DataHandler
from datetime import datetime, timedelta

def main():
    # Create an instance of DataHandler
    data_handler = DataHandler()

    # Example usage of query_bigquery
    start_time = datetime.now() - timedelta(days=20)
    end_time = datetime.now()
    data = data_handler.query_bigquery(start_time=start_time, end_time=end_time)
    geo_data = data_handler.site_geolocation_data(data)
    if geo_data is not None:
 
        
        print(geo_data.head())  # Example: Print the first few rows of the site geolocation data
    else:
        print("Error occurred while querying BigQuery.")

if __name__ == "__main__":
    main()
