import CloudFlare, requests, os, datetime, sys

def get_wan_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data     = response.json()
        wan_ip   = data['ip']
        
        return wan_ip
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred: {e}")

def get_domain_from_fqdn(fqdn):
    parts        = fqdn.split(".")
    domain_parts = parts[1:]
    domain_name  = ".".join(domain_parts)

    return domain_name

def get_host_from_fqdn(fqdn):
    parts   = fqdn.split(".")
    host    = parts[0]

    return host

def main():
    # Get arguments from environment variables.
    # NOTE: CLOUDFLARE_API_TOKEN should be set.
    fqdn    = os.environ.get("CLOUDFLARE_DDNS_HOSTNAME")
    domain  = get_domain_from_fqdn(fqdn)
    wan_ip  = os.environ.get("CLOUDFLARE_DDNS_WANIP")

    # Get our WAN interface IP if it hasn't been defined.
    if not wan_ip:
        wan_ip = get_wan_ip()

    # Get formatted time/date
    current_date = datetime.datetime.now() 
    formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    # Call Cloudflare API and update record.
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params={ 'name':  domain})
    if len(zones) == 1:
        zone_id = zones[0]['id']
    elif len(zones) == 0:
        # No matching domain
        sys.exit("Domain not found for DDnS entry.")
    else:
        # Something else is wrong.
       sys.exit(f"Unknown reason for failure. {zones}")
    
    records = cf.zones.dns_records.get(zone_id, params={ 'name': fqdn})

    record_data = {
        "content": wan_ip,
        "name": fqdn,
        "type": "A",
        "comment": f"Automatically updated record via Python DDNS client. Last update: { formatted_date }"
    }

    if len(records) == 0:
        # Create a new record with IP.
        cf.zones.dns_records.post(zone_id, data=record_data)
        print(f"Created new DDnS entry, {fqdn}, with IP {wan_ip}")
    else:
        # Check to see if IP has changed, if so, update. If not, do nothing.
        if not records[0]['content'] == wan_ip:
            cf.zones.dns_records.put(zone_id, records[0]['id'], data=record_data)
            print(f"Updated DDnS entry, {fqdn}, with IP {wan_ip}")
        print(f"No updated needed for {fqdn}")

if __name__ == '__main__':
    main()    