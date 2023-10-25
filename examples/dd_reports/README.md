# Overview
This is a set of python scripts that connect to the Red Cloak portal and generate csv reports for FCM change events,
and hosts which are actively connecting and those that are not actively connecting.


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
Generate CSV file of FCM events based on a date/time combination:
```
usage: dd_reports fcm_events_report [-h] --start START --end END --key KEY
                                    --domain DOMAIN --output OUTPUT

optional arguments:
  -h, --help       show this help message and exit

required arguments:
  --start START    Start date and time in format: yyyy-mm-ddThh:mm:ss
  --end END        End date and time in format: yyyy-mm-ddThh:mm:ss
  --key KEY        Red Cloak API key
  --domain DOMAIN  Domain ID to run report for
  --output OUTPUT  Filename to save output to
```

Generate CSV file of endpoints which *have not* connected in the last 12 hours:
```
usage: dd_reports out_of_contact_report [-h] --key KEY --domain DOMAIN
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
usage: dd_reports in_contact_report [-h] --key KEY --domain DOMAIN --output
                                    OUTPUT

optional arguments:
  -h, --help       show this help message and exit

required arguments:
  --key KEY        Red Cloak API key
  --domain DOMAIN  Domain ID to run report for
  --output OUTPUT  Filename to save output to

```

# Examples
To generate a daily report it is important to remember that ALL timestamps in Red Cloak are UTC. If you want to search for events between 8am ET - 8am ET, you need to add 5 hours (4 hours during Daylight Savings Time).
```
python.exe dd_reports.py fcm_events_report --start 2018-01-17T13:00:00 --end 2018-01-18T13:00:00 --domain 6bb9f19b --key <API key file> --output daily-2018-01-17.csv
```

Weekly report...
```
python.exe dd_reports.py fcm_events_report --start 2018-01-08T13:00:00 --end 2018-01-14T13:00:00 --domain 6bb9f19b --key <API key file> --output weekly-2018-01-08.csv
```

To generate a report of all of the endpoints which have not communicated in at least 12 hours.
```
python.exe dd_reports.py out_of_contact_report --domain 6bb9f19b --key key.json --output out_of_contact-2018-01-19.csv
```

To generate a report of all the endpoints which are actively connecting.
```
python.exe dd_reports.py in_contact_report --domain 6bb9f19b --key key.json --output in_contact-2018-01-19.csv
```