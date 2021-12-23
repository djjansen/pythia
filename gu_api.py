import requests
import json

base_url = 'https://api.godsunchained.com/v0'
address = '0x3882'


#get_inventory = requests.get('https://api.godsunchained.com/v0/user/0xff18298382948028f9d93c4e32be1382204022c8')

#print(get_inventory.text)

test = requests.get(f'{base_url}/card?order_by=id&user={{wallet}}')

print(test.text)


