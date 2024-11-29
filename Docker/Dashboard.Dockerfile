# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Copy Python scripts
COPY ../app.py /app/
COPY ../DataImport.py /app/
COPY ../ProcessTrips.py /app/

# Copy the required data files
COPY ../yellow_tripdata_2019-01_full.csv /app/
COPY ../taxi+_zone_lookup.csv /app/

# Copy the requirements file
COPY ../Dashboard_requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r Dashboard_requirements.txt

# Expose port 8501
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
