myauthtoken = 'MYTOKENGOESHERE'

from cloudgenix import API, jd

sdk = API()

sdk.interactive.use_token(myauthtoken)

response = sdk.get.sites()

site_list = response.cgx_content.get("items")

tag_input = ""
while (tag_input == ""):
    tag_input = str(input("Please Enter the site TAG you would like to use: "))

for site in site_list:
    print("Site Name", site['name'])
    print("Current Site Tags", str(site['tags']))
    print (" ")

    user_input = ""
    while (user_input != "y" and user_input != "n"):
        user_input = str(input("Would you like to add the tag to this site (y/n)? "))
    
    if (user_input == "y"):
        site['tags'].append(tag_input)
        put_response = sdk.put.sites(site['id'],site)
        print("Added Tag Successfully")
    print(" ")
