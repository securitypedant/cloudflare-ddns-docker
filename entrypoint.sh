#!/bin/bash

# Start the cron daemon in the background
cron

# Use the value of CRON_SCHEDULE environment variable or default to every minute
SCHEDULE="${CRON_SCHEDULE:-*/1 * * * *}"

# Schedule the Python script to run based on the environment variable
echo "$SCHEDULE python /app/script.py >> /var/log/cron.log 2>&1" | crontab -

# Keep the container running
tail -f /dev/null