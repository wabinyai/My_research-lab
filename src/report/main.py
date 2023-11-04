from configure import BIGQUERY_CONSOLIDATED_DATA
from utility import run_bigquery_query

if __name__ == "__main__":
    start_time = '2023-11-03'  # Updated start_time
    end_time = '2023-11-03'    # Updated end_time

    query = (
        f"SELECT TIMESTAMP_SECONDS(EXTRACT(EPOCH FROM timestamp)) as hour, "
        f"EXTRACT(DATE FROM timestamp) as date, EXTRACT(MONTH FROM timestamp) as month, "
        "pm2_5_calibrated_value, city "
        f"FROM `{BIGQUERY_CONSOLIDATED_DATA}` "
        f"WHERE TIMESTAMP_TRUNC(timestamp, MONTH) >= TIMESTAMP('{start_time}') "
        f"AND TIMESTAMP_TRUNC(timestamp, MONTH) <= TIMESTAMP('{end_time}') "
        f"AND city = 'Kampala'"
    )

    json_results = run_bigquery_query(query)
    print(json_results)
