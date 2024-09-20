# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to reduce Python's buffer for more efficient logging
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
WORKDIR /app

# Copy the current directory (where your script is) to /app in the container
COPY . /app

# Install requirements - NOTE: --no-cache-dir prevents pip from storing downloaded files in local cache (reduces image size).
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the Python script
CMD ["python", "main.py"]
