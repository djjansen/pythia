import dash
from dash import dcc
from dash import html
import plotly.express as px

import pandas as pd
from pandas.io.json import json_normalize
import json

import imx_api

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

cards_df = pd.DataFrame(imx_api.get_card_collection(wallet="{{wallet}}"))
metadata_series = cards_df['metadata'].apply(lambda x: json_normalize(x))
metadata_cols = pd.concat(list(metadata_series), ignore_index=True, sort=True)
combined_cards_df = cards_df.drop(columns=["name"]).join(metadata_cols)
combined_cards_df['token_id'] = pd.to_numeric(combined_cards_df['token_id'])

total_cards_by_set = combined_cards_df.pivot_table(index="set", columns="god", values="token_id", aggfunc="count").reset_index()
total_cards_by_set['total'] = total_cards_by_set.sum(axis=1, skipna=True)

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