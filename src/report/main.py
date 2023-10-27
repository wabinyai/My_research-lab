from configure import BIGQUERY_CONSOLIDATED_DATA
from utility import run_bigquery_query

if __name__ == "__main":
    start_time = '2023-06-01'
    end_time = '2023-09-30'

    query = (
        f"SELECT * FROM `{BIGQUERY_CONSOLIDATED_DATA}` "
        f"WHERE TIMESTAMP_TRUNC(timestamp, MONTH) >= TIMESTAMP('{start_time}') "
        f"AND TIMESTAMP_TRUNC(timestamp, MONTH) <= TIMESTAMP('{end_time}') "
        "LIMIT 10"
    )
    
    json_results = run_bigquery_query(query)
