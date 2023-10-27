from google.cloud import bigquery
import json

def run_bigquery_query(query):
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()

    # Convert query results to a list of dictionaries
    results_list = [dict(row) for row in results]

    # Return results as JSON
    return json.dumps(results_list)

if __name__ == "__main__":
    query = "Your SQL Query Here"
    result = run_bigquery_query(query)
    print(result)
    print("Successful")
