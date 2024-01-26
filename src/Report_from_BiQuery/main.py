from datetime import datetime
from utils import fetch_air_quality_data, query_bigquery, results_to_dataframe, calculate_mean_daily_pm2_5, calculate_mean_pm2_5_by_site_name

def main():
    grid_id = "64b7f325d7249f0029fed743"
    start_time = datetime(2023, 12, 26, 9, 0, 0)
    end_time = datetime(2024, 1, 1, 12, 0, 0)

    site_ids = fetch_air_quality_data(grid_id, start_time, end_time)
    if site_ids:
        results = query_bigquery(site_ids, start_time, end_time)
        if results is not None:
            processed_data = results_to_dataframe(results)
            daily_mean_pm2_5 = calculate_mean_daily_pm2_5(processed_data)
            site_mean_pm2_5 = calculate_mean_pm2_5_by_site_name(processed_data)

            # Prepare the response data in a structured format
            response_data = {
                'status': 'success',
                'grid_id': grid_id,
                'site_ids': site_ids,
                'period': {
                    'startTime': start_time.isoformat(),
                    'endTime': end_time.isoformat(),
                },
                'daily_mean_pm2_5': daily_mean_pm2_5.to_dict(),
                'site_mean_pm2_5': site_mean_pm2_5.to_dict(),
            }

            # Print the response data as JSON
            print(response_data)

if __name__ == "__main__":
    main()
