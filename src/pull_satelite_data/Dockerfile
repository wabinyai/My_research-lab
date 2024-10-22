# Use the official Airflow image as the base image
FROM apache/airflow:2.1.3-python3.9

# Set the working directory in the container
WORKDIR /app
# Copy the requirements file and install dependencies
COPY requirements.txt /requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy your Python scripts into the container
COPY configure.py pull_satelite_data/configure.py
COPY utils.py pull_satelite_data/utils.py
COPY pullsatelite_main.py pull_satelite_data/pullsatelite_main.py 
COPY app.py pull_satelite_data/app.py 
# Expose the port for the Airflow webserver (optional)
EXPOSE 8080

# Set the working directory

# Set the entrypoint to start the Airflow webserver
CMD ["python", "main_test.py"]
ENTRYPOINT ["airflow", "webserver", "--port", "8080", "--host", "0.0.0.0"]
 