# Use an official Python image
FROM python:3.9

# Install netcat-openbsd to allow for waiting on PostgreSQL service
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install pandas sqlalchemy psycopg2-binary

# Make wait-for-postgres.sh executable
RUN chmod +x /app/wait-for-postgres.sh

# Run DataExporter.py after PostgreSQL is ready
CMD ["/app/wait-for-postgres.sh", "postgres", "5432", "python", "DataExporter.py"]
