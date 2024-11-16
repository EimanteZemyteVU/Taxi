# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy Dashboard_requirements.txt from the parent directory into the container
COPY ../Dashboard_requirements.txt /app/

# Install any needed packages specified in Dashboard_requirements.txt
RUN pip install --no-cache-dir -r Dashboard_requirements.txt

# Copy app.py from the parent directory into the container
COPY ../app.py /app/

# Expose port 8501 (the default port for Streamlit)
EXPOSE 8501

# Run Streamlit when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]