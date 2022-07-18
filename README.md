# netbox-to-hosts
Syncs devices that have a Primary IP allocated from [Netbox](https://netbox.readthedocs.io/en/stable/) to /etc/hosts on the given system. Designed to run via cron periodically.

## Compatibility
Requires: python3.x & requests module

## Installation Example

1. Clone the repository and copy the `netbox-to-hosts` folder to `/opt`
```
git clone https://github.com/jasonyates/netbox-to-hosts.git

sudo cp -r netbox-to-hosts/ /opt
cd /opt/netbox-to-hosts
```
2. Install python requirements
```
pip install -r requirements.txt
```

3. Update script settings. Set your Netbox URL, filter & limit settings. Default settings will only sync devices that are marked active, and have the tags network & managed.
```
netboxURL = 'yournetboxinstance.com'
netboxFilter = 'tag=network&tag=managed&status=active'
netboxLimit = '3000'
```

4. Login to netbox and generate an API token in your profile (recommended to disable write operations for the API key)

5. Test syncing device data to /etc/hosts - replace the example API key with your own - MUST run as root to have write access to /etc/hosts
```
sudo /opt/netbox-to-hosts/netbox2hosts.py af5c08ec8124a38c1d81435fg0548b8529fa6b63
```

6. (Optional) Add a crontab entry as root to sync device data from netbox
```
sudo crontab -e

*/5 * * * * /opt/netbox-to-hosts/netbox2hosts.py <apikey>