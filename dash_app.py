import dash
from dash import dcc
from dash import html
import plotly.express as px

import pandas as pd
from pandas.io.json import json_normalize
import json

import imx_api
import gu_api

app = dash.Dash(__name__)


# IMPORT IMX DATA
wallet = 'x'
# get list of cards owned
cards_df = pd.DataFrame(imx_api.get_card_collection(wallet=wallet))
# split metadata nested json into separate columns
metadata_series = cards_df['metadata'].apply(lambda x: json_normalize(x))
metadata_cols = pd.concat(list(metadata_series), ignore_index=True, sort=True)
combined_cards_df = cards_df.drop(columns=["name"]).join(metadata_cols)
# cast token_id to numeric for pivoting
combined_cards_df['token_id'] = pd.to_numeric(combined_cards_df['token_id'])

# create pivot table of card total by god and set
total_cards_by_set = combined_cards_df.pivot_table(index="set", columns="god", values="token_id", aggfunc="count").reset_index()
total_cards_by_set['total'] = total_cards_by_set.sum(axis=1, skipna=True)


# IMPORT GU DATA
player_id = 'x'
# get list of games played
games_won = gu_api.make_gu_api_call('GET', f'/match?player_won={player_id}&perPage=200&sort=start_time&order=asc')
games_lost = gu_api.make_gu_api_call('GET', f'/match?player_lost={player_id}&perPage=200&sort=start_time&order=asc')
games_played = games_won + games_lost
# flatten player_info to add as df columns
player_info = []
for game in games_played:
    player_info_row = {}
    for player in game['player_info']:
        if player['user_id'] == player_id:
            prefix = 'own_'
        else:
            prefix = 'opponent_'
        for field in player:
            player_info_row[prefix + field] = player[field]
    player_info.append(player_info_row)
    game.pop('player_info')

games_played_full = [{**game_info, **player_info} for game_info, player_info in zip(games_played, player_info)]
games_played_df = pd.DataFrame(games_played_full)
# cards by set bar chart
fig = px.bar(total_cards_by_set, x="set", y="total", color="set")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)