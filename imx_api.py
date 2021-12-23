import requests
import json

url = "https://api.x.immutable.com/v1/assets?page_size=1000&user={{wallet}}&sell_orders=true&order_by=name&direction=asc"
# note: cursor at end of response JSON needs to be added to subsequent request to page through results

headers = {"Accept": "application/json"}


response = requests.request("GET", url, headers=headers)


print(len(json.loads(response.text)['result']))
print(json.loads(response.text))
