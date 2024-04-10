# Use the official Airflow image as the base image
FROM python:3.9-slim
FROM apache/airflow:2.1.3-python3.9

# Copy the requirements file and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy your Python scripts into the container
COPY utils.py /usr/local/airflow/utils.py
COPY main_workflow.py /usr/local/airflow/dags/main.py
COPY configure.py /usr/local/airflow/configure.py

# Expose the port for the Airflow webserver (optional)
EXPOSE 5000

# Set the working directory

# Set the entrypoint to start the Airflow webserver
ENTRYPOINT ["airflow", "webserver", "--port", "5000", "--host", "0.0.0.0"]
 

 
EXPOSE 5000