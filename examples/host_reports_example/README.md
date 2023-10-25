# Overview
This is a set of python scripts that connect to the Red Cloak portal and generate an example of a CSV report for hosts which are actively connecting and those that are not actively connecting.


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
Generate CSV file of endpoints which *have not* connected in the last 12 hours:
```
usage: host_reports_example out_of_contact_report [-h] --key KEY --domain DOMAIN
                                        --output OUTPUT

optional arguments:
  -h, --help       show this help message and exit

required arguments:
  --key KEY        Red Cloak API key
  --domain DOMAIN  Domain ID to run report for
  --output OUTPUT  Filename to save output to
```

Generate CSV file of endpoints which *have* connected in the last 12 hours:
```
usage: host_reports_example in_contact_report [-h] --key KEY --domain DOMAIN --output
                                    OUTPUT

optional arguments:
  -h, --help       show this help message and exit

required arguments:
  --key KEY        Red Cloak API key
  --domain DOMAIN  Domain ID to run report for
  --output OUTPUT  Filename to save output to

```

# Examples
To generate a report of all of the endpoints which have not communicated in at least 12 hours.
```
python.exe host_reports_example.py out_of_contact_report --domain <domain_id> --key key.json --output out_of_contact-2018-01-19.csv
```

To generate a report of all the endpoints which are actively connecting.
```
python.exe host_reports_example.py in_contact_report --domain <domain_id> --key key.json --output in_contact-2018-01-19.csv
```