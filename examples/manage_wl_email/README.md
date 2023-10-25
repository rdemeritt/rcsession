# Overview
This is a set of python scripts that connect to the Red Cloak portal and add/remove email addresses from watchlist subscription notifications.


# Requirements
python 3.5
rcsession 0.3.1 (<https://stash.secureworks.net/users/rdemeritt/repos/rcsession>)

You will also need to setup an API-GW key and place it in a JSON file used for the `--key` option:
```json
{
    "key": "rdemeritt@gmail.com:s0m3P@$$w0rd"
}
```

# Usage
Add or remove email address(es) from a watchlist notification:
```
usage:  [-h] [--log_level LOG_LEVEL] --key KEY --wl_id WL_ID --email EMAIL
        [--add | --delete] --domain_id DOMAIN_ID

optional arguments:
  -h, --help            show this help message and exit
  --log_level LOG_LEVEL
                        Set the logging level
  --key KEY             Red Cloak API key
  --wl_id WL_ID         Watchlist ID you wish to manage
  --email EMAIL         Email address to add/remove
  --add                 Add email to watchlist subscription notification
  --delete              Remove email from watchlist subscription notification
  --domain_id DOMAIN_ID
                        Domain ID to be notified on
```

# Examples
To add rdemeritt@gmail.com as a person to be notified when watchlist_id 48649832-2e08-4882-aa66-db022349c177 has triggered for domain_id d32c7944.
```
python.exe manage_wl_email.py --key key.json --log_level debug  --add --wl_id 48649832-2e08-4882-aa66-db022349c177 --domain_id d32c7944 --email "rdemeritt@gmail.com"
```

Remove rdemeritt@gmail.com from the list of persons to be notified when watchlist_id 48649832-2e08-4882-aa66-db022349c177 has triggered for domain d32c7944
```
python.exe manage_wl_email.py --key key.json --log_level debug  --delete --wl_id 48649832-2e08-4882-aa66-db022349c177 --domain_id d32c7944 --email "rdemeritt@gmail.com"
```
