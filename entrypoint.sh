#!/bin/bash

# Store environment for cron
printenv | grep -v "no_proxy" >> /etc/environment

# Start the cron daemon in the background
cron

# Use the value of CRON_SCHEDULE environment variable or default to every minute
SCHEDULE="${CRON_SCHEDULE:-*/0 1 * * *}"

# Schedule the Python script to run based on the environment variable
echo "$SCHEDULE /usr/local/bin/python3 /app/cloudflare-ddns.py >> /var/log/cron.log 2>&1" | crontab -

# Keep the container running
tail -f /dev/null