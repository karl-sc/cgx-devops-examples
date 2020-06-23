#####################################
## You need to provide tier-1 staff a mechanism to add static routes to any branch without granting full access to the interface.
## Create a script which takes an IP address, Site Name, and Next-Hop as an input and adds it to that branches routing table
#####################################


### INPUT ###
# Authenticate
# Read CLI Arguments [IP Subnet, Next-Hop, Site-Name]

CLOUDGENIX_AUTH_TOKEN = '[put your token here]'
from cloudgenix import API

sdk = API()
sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)

import sys

if len(sys.argv) != 4:
    sys.exit("Usage: add-route.py [destination-subnet] [next-hop] [sitename]")

site_name = sys.argv[3]


## SYSTEM ###
# Connect to SDK
# Verify the IP Subnet, Next-Hop, and Site Name

import ipaddress
try:
    ip_dest = ipaddress.ip_network(sys.argv[1], strict=False)
    ip_gw = ipaddress.ip_address(sys.argv[2])
except:
    sys.exit("IP Address/subnet not in correct format")

result = sdk.get.sites()
if result.cgx_status is not True:
    sys.exit("API ERROR!!!")

site_id = None
for site in result.cgx_content.get("items"):
    if site_name == site['name']:
        site_id = site['id']

if site_id == None:
    sys.exit("Site Name Not Found ERROR!!!")

element_to_change = []

result = sdk.get.elements()
for element in  result.cgx_content.get("items"):
    if element['site_id'] == site_id:
        element_to_change.append(element)


### INPUT ###
# Verify the addition with the User

user_input = ""
while user_input != "y" and user_input != "n":
    print("this change will affect",len(element_to_change),"elements at the site, Proceed? (y/n): ")
    user_input = input("(y/n)")

if user_input == "n":
    sys.exit("Operation cancelled by user")

### INPUT ###
# Use the API/SDK to write the static route
# Write success to console

post_data = '{"description":null,"tags":null,"destination_prefix":"' + str(ip_dest) + '","nexthops":[{"nexthop_ip":"' + str(ip_gw) + '","nexthop_interface_id":null,"admin_distance":1,"self":false}],"scope":"local","network_context_id":null}'
for element in element_to_change:
    result = sdk.post.staticroutes(site_id, element['id'], post_data)
    if result.cgx_status is not True:
        print("Static Route addition failed")
    else:
        print("Static Route addition SUCCESS")

