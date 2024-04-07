from datetime import datetime
from utils import fetch_air_quality_data, datetime_pm2_5,mean_pm2_5_by_month_year,mean_pm2_5_by_month_name,query_bigquery, mean_pm2_5_by_month,results_to_dataframe,mean_pm2_5_by_year, mean_daily_pm2_5, mean_pm2_5_by_site_name,mean_pm2_5_by_hour

def main():
    grid_id = "64b7f325d7249f0029fed743"
    start_time = datetime(2023, 12, 14, 9, 0, 0)
    end_time = datetime(2024, 1, 15, 12, 0, 0)

    site_ids = fetch_air_quality_data(grid_id, start_time, end_time)
    if site_ids:
        results = query_bigquery(site_ids, start_time, end_time)
        if results is not None:
            processed_data = results_to_dataframe(results)
            daily_mean_pm2_5 = mean_daily_pm2_5(processed_data)
            datetime_mean_pm2_5 = datetime_pm2_5(processed_data)
            site_mean_pm2_5 = mean_pm2_5_by_site_name(processed_data)
            hour_mean_pm2_5 = mean_pm2_5_by_hour(processed_data)
            mean_pm2_5_year= mean_pm2_5_by_year(processed_data)
            pm2_5_by_month =mean_pm2_5_by_month(processed_data)
            pm2_5_by_month_name =mean_pm2_5_by_month_name(processed_data)
            pm2_5_by_month_year = mean_pm2_5_by_month_year(processed_data)#
#            print(pm2_5_by_month_year)

            # Prepare the response data in a structured format
            response_data = {
                'air_quality': {
                'status': 'success',
                'grid_id': grid_id,
               'site_ids': site_ids,
               'period': {
                   'startTime': start_time.isoformat(),
                    'endTime': end_time.isoformat(),
                },
               'daily_mean_pm': daily_mean_pm2_5.to_dict(orient='records'),
               'datetime_mean_pm': datetime_mean_pm2_5.to_dict(orient='records'),
                'site_mean_pm': site_mean_pm2_5.to_dict(orient='records'),
                'hour_mean_pm': hour_mean_pm2_5.to_dict(orient='records'),
                'mean_pm_year': mean_pm2_5_year.to_dict(orient='records'),
                'pm_by_month': pm2_5_by_month.to_dict(orient='records'),
                'pm_by_month_year':pm2_5_by_month_year.to_dict(orient='records'),
                'pm_by_month_name': pm2_5_by_month_name.to_dict(orient='records'),
                },

                    
            }

            # Print the response data as JSON
            print(response_data)

if __name__ == "__main__":
    main()
