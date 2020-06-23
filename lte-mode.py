#####################################
## Management has decided that the current cost of LTE is too high and wants you to de-prioritize its usage for all sites using it.
## Create a script which matches WAN interfaces and changes: 
##      - WAN Cost
##      - Toggles Link-Quality-Monitoring Metrics
##      - Toggles Bandwidth/Path Capacity Monitoring
##      - Toggles Aggressive BFD on the tunnels
#####################################


### INPUT ###
# Authenticate
# Read CLI Arguments Interface Match, Weight , LTE ‘mode’ Toggle ON

CLOUDGENIX_AUTH_TOKEN = '[put your token here]'
from cloudgenix import API

sdk = API()
sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)

import sys

if len(sys.argv) != 4:
    sys.exit("Usage: lte-mode.py [interfacematch] [cost] [ltemode (0/1)]")

interface_match = sys.argv[1]
cost = sys.argv[2]
if sys.argv[3] == "0":
    lte_mode = False
elif sys.argv[3] == "1":
    lte_mode = True
else:
    sys.exit("Usage: lte-mode.py [interfacematch] [cost] [ltemode (0/1)]")

## SYSTEM ###
# Connect to SDK
# Retrieve all WAN interfaces
#   Match interface based on interface match parameter and store in array 

result = sdk.get.sites()
if result.cgx_status is not True:
    sys.exit("API ERROR!!!")

for site in result.cgx_content.get("items"):
    result = sdk.get.waninterfaces(site['id'])
    if result.cgx_status is True:
        for waninterface in result.cgx_content.get("items"):
            if interface_match.lower() in waninterface['name'].lower():
### INPUT ###
# Verify the addition with the User
                user_input = ""
                while user_input != "y" and user_input != "n":
                    print("this change will affect",waninterface['name'])
                    user_input = input("Proceed? (y/n): ")
                if user_input == "y":
 ### INPUT ###
# Iterate array and use SDK on each to make change
# Write success to console
                    if lte_mode == True:
                        waninterface['cost'] = cost
                        waninterface['lqm_enabled'] = 'false'
                        waninterface['bw_config_mode'] = 'manual_bwm_disabled'
                        waninterface['bfd_mode'] = "non_aggressive"
                    if lte_mode == False:
                        waninterface['cost'] = cost
                        waninterface['lqm_enabled'] = 'true'
                        waninterface['bw_config_mode'] = 'manual'
                        waninterface['bfd_mode'] = "aggressive"
                    result = sdk.put.waninterfaces(site['id'],waninterface['id'],waninterface)
                    if result.cgx_status is True:
                        print("LTE Change Success")
                    else:
                        print("FAILURE on Changing")






