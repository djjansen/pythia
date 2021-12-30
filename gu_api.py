import requests
import json

base_url = 'https://api.godsunchained.com/v0'

games_won = requests.get(f'{base_url}/match?player_won=XXXXXXX&page=1&perPage=200&start_time=1640311200-1640570399&sort=start_time&order=asc')

games_won = json.loads(games_won.text)

print(games_won)


