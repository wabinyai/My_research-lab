# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment (Linux/MacOS)
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

# (Windows) Uncomment the line below and comment out the above two lines
 RUN venv\scripts\activate

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose any necessary ports
EXPOSE 80

# Set environment variable for Airqloud ID
ENV AIRQLOUD_ID "Your_Airqloud_ID_Here"

# Command to run the application
CMD ["python", "main.py"]



docker build -t local-moran .