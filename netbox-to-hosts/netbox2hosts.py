#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Jason Yates <me@jasonyates.co.uk>
# version ='1.0'
# Description : Syncs inventory from Netbox to /etc/hosts using python requests module. Run periodically via CRON.
# Requires : Netbox API key. Recommended not to be write enabled.
# Execute : netbox2hosts.py <api-key> e.g. netbox2hosts.py 3ea67011eadd3cbb8ef8523d37adcd67517a6743
# ---------------------------------------------------------------------------

from os import write
import requests
import os.path
from datetime import datetime
import sys

#----------------------------------------------------------------------------
# Settings
#----------------------------------------------------------------------------
netboxURL = ''
netboxFilter = 'tag=network&tag=managed&status=active'
netboxLimit = '3000'
writeFile = '/etc/hosts'
requestVerify = False
requestTimeout = 10

# Get API key from CLI
if len(sys.argv) == 1:
    print("ERROR: No netbox API key specified")
    exit(0)
elif len(sys.argv[1]) < 20:
    print("ERROR: Invalid netbox API key specified")
    exit(0)
else:
    netboxAPIKey = sys.argv[1]

# Sync devices from Netbox and write them to specified file in a standard host file format
def syncNetbox():

    # Check we can write to the file. Usually /etc/hosts so need root
    if check_file_writable(writeFile) == True:

        # Call netbox
        r=requests.get(netboxURL + "/api/dcim/devices/?" + netboxFilter + "&limit=" + netboxLimit, headers={"Authorization":"Token " + netboxAPIKey}, verify=requestVerify, timeout=requestTimeout)

        # Check we got a valid response
        if r.status_code == 200:

            # Check we got some devices returned
            if "count" in r.json() and r.json()['count'] > 1:

                try:
                    with open(writeFile, 'w') as f:

                        # Write file header
                        f.write(getFileHeader(r.json()['count']))

                        # Loop netbox devices
                        for device in r.json()['results']:

                            if device['primary_ip4'] != None and "display" in device['primary_ip4']:

                                # Format the IP and write the line to file
                                primary_ip = device['primary_ip4']['display'].split("/")
                                f.write(primary_ip[0] + " " + device['name']+ "\n")

                        # Close file
                        f.close()

                        # Finished
                        print("Done. " + str(r.json()['count']) + " hosts written to " + writeFile)

                except IOError as x:
                    print ("ERROR: No permission to write to file " + writeFile)

            else:
                print("ERROR: Invalid response from Netbox. No devices returned")    

        else:
            print("ERROR: Invalid HTTP response from Netbox. Statuscode " + str(r.status_code))

    else:
        print ("ERROR: No permission to write to file " + writeFile)

def getFileHeader(count):

    # Get the header details
    header = "# File auto generated by netbox2hosts.py\n"
    header = header + "# Data pulled via API from " + netboxURL +"\n"
    header = header + "# Last Update: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
    header = header + "# No. Devices: " + str(count) + "\n\n"
    header = header + "127.0.0.1 localhost\n"
    header = header + "::1 localhost\n\n"
    header = header + "### DO NOT MANUALLY EDIT THIS FILE. IT WILL BE OVERWRITTEN PERIODICALLY\n\n"

    return header

def check_file_writable(fnm):
    if os.path.exists(fnm):
        if os.path.isfile(fnm):
            return os.access(fnm, os.W_OK)
        else:
            return False
    pdir = os.path.dirname(fnm)
    if not pdir: pdir = '.'
    return os.access(pdir, os.W_OK)

if __name__ == '__main__':
    syncNetbox()