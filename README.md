# Simple Docker image to update a Cloudflare record with your network WAN IP

This is a super simple DDNS client written in Python and published as a docker image.
It requires you have a Cloudflare account and an API token with the following permissions.

- Zone - Zone - Edit
- Zone - DNS - Edit

You must also set the following Docker image environment variables

- CLOUDFLARE_API_TOKEN = "YOURAPITOKEN"
- CLOUDFLARE_DDNS_HOSTNAME = "host.domain.com"
- CLOUDFLARE_DDNS_WANIP = "1.2.3.4"

Where the HOSTNAME is the A record you wish to create/update in Cloudflare and the WANIP if you already know the IP and just want to use this to set it.

Build the Docker image with
docker buildx build --platform linux/amd64,linux/arm64 --push -t simonsecuritypedant/cloudflare-ddns:1.0 -f Dockerfile .

To run using Docker, create the following compose.yaml

version: '2'
services:
  cloudflare-ddns:
    image: simonsecuritypedant/cloudflare-ddns:latest
    restart: always
    environment:
      - CLOUDFLARE_API_TOKEN=xxxxxxx
      - CLOUDFLARE_DDNS_HOSTNAME=host.example.com
      - CLOUDFLARE_DDNS_WANIP=1.2.3.4
      - CRON_SCHEDULE="*/10 * * * *"
