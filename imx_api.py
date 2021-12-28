import requests
import json
import pandas as pd

url = "https://api.x.immutable.com/v1/assets?page_size=1000&user={{wallet}}&sell_orders=true&order_by=name&direction=asc"
# note: cursor at end of response JSON needs to be added to subsequent request to page through results

headers = {"Accept": "application/json"}


def make_imx_api_call(method, endpoint, headers=headers, payload=None, prior_results=None):
    response = requests.request(method, endpoint, headers=headers)
    response_json = json.loads(response.text)
    # start empty result set
    if prior_results is None:
        total_results = response_json['result']
    else:
        prior_results.extend(response_json['result'])
        total_results = prior_results
    # if more results remain, page through
    if response_json['remaining'] == 1:
        make_imx_api_call(method, endpoint+f'&cursor={response_json["cursor"]}',
                          prior_results=total_results)
    return total_results


df = pd.DataFrame(make_imx_api_call("GET", url))
df.to_csv('my_cards.csv')

