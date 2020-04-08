myauthtoken = 'TOKENHERE'

from cloudgenix import API, jd

sdk = API()

sdk.interactive.use_token(myauthtoken)

#jd(sdk.get.sites())

event_request = {"limit":{"count":5,"sort_on":"time","sort_order":"descending"},"query":{"type":["alarm"]},"view":{"summary":False},"severity":[],"acknowledged":True}

response = sdk.post.events_query(event_request)

alarm_list = response.cgx_content.get("items")

for alarm in alarm_list:
    print("=================")
    print("ALARM     :" + alarm['code'] )
    print("  TIME    :" + alarm['time'] )
    print("  SEVERITY:" + alarm['severity'] )
    print("=================")
    print(" ")
