# Use a base image with Python installed
FROM python:3.8-slim

# Copy the Python script and entrypoint script to the container
COPY cloudflare-ddns.py /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/

# Set the working directory
WORKDIR /app

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Install any additional dependencies for your Python script if needed
RUN pip install -r requirements.txt

# Set an environment variable for the cron schedule (default to every minute)
ENV CRON_SCHEDULE "*/1 * * * *"

# Run the entrypoint script when the container starts
CMD ["./entrypoint.sh"]