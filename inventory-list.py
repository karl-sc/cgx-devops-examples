#####################################
## Your Inventory Specialist has asked for a list of all hardware appliances with hostname, serial number, and software version
## Create a script which can export all ION hardware devices to a CSV list
#####################################

### INPUT ###
# Authenticate 
# Read CLI Arguments [output CSV File]

CLOUDGENIX_AUTH_TOKEN = '[put your token here]'
from cloudgenix import API

sdk = API()
sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)

import sys

if len(sys.argv) != 2:
    sys.exit("Usage: inventory-list.py [csvfilename]")

csv_filename = sys.argv[1]

### SYSTEM ###
# Connect to SDK
# Retrieve all elements
#	Store elements and data in a 2-Dimensional Array

result = sdk.get.elements()
if result.cgx_status is not True:
    sys.exit("API Error!")


csv_out_array = []
csv_out_array.append( [ "name", "serial", "software-version" ])

for element in result.cgx_content.get("items"):
    csv_out_array.append( [  element['name'], element['serial_number'], element['software_version'] ]  )


### OUTPUT ###
# Create the output CSV File and write with format name, serial_number, software_version
# Write to console success

import csv
with open(csv_filename,"w") as myfile:
    csv_writer = csv.writer(myfile)
    csv_writer.writerows(csv_out_array)
print("File written succesfully!!")


