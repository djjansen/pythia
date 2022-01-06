import requests
import json

base_url = 'https://api.godsunchained.com/v0'
headers = {"Accept": "application/json"}


def make_gu_api_call(method, endpoint, headers=headers, payload=None, prior_results=None, page=1):
    response = requests.request(method, base_url + endpoint + f'&page={page}', headers=headers)
    response_json = json.loads(response.text)
    # start empty result set
    if prior_results is None:
        total_results = response_json['records']
    else:
        prior_results.extend(response_json['records'])
        total_results = prior_results
    # if more results remain, page through
    if len(total_results) < response_json['total']:
        make_gu_api_call(method, endpoint, page=page+1, prior_results=total_results)
    return total_results


# card_reference = requests.get(f'{base_url}/proto/1210')
# card_reference = json.loads(card_reference.text)
