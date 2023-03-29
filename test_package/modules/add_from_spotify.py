import pandas as pd
from test_package.modules.api_request import get_spotify_df
from test_package.modules.engineering import add_artists_clean
from test_package.modules.registry import load_data_to_bq
from test_package.params import *

'''
This module uses the Spotify API to get new songs - both when an unkown song is
"Shazamed" and when the user wants to update the database.
'''

def get_new_songs(data, artist_name, song_name=""):
    new_data = get_spotify_df(f"{artist_name} - {song_name}")
    for i, row in new_data.iterrows():
        new_row = pd.DataFrame(columns=data.columns).drop(columns=["artists_clean"])
        new_row.loc[0,row.index] = row
        new_row=new_row.fillna("1").astype(GET_SPOTIFY_DTYPES)
        if PROJECT_STATE=="cloud":
            load_data_to_bq(new_row, GCP_PROJECT, BUCKET_NAME, 'raw_data', False)
        new_row['name'] = new_row['name'].str.lower()
        new_row['artists'] = new_row['artists'].str.lower()
        new_row = add_artists_clean(new_row)
        data = pd.concat([data, new_row], ignore_index=False, axis=0)
        data.reset_index(inplace=True, drop=True)
    return data

def fill_missing_artists(data, artist_list):
    assert 'artists_clean' in data.columns, "data frame doesnt have artists_clean column. See add_artists_clean"

    for artist in artist_list:
        if artist not in data['artists_clean'].values:
            new_data = get_spotify_df(artist)
            for i, row in new_data.iterrows():
                new_row = pd.DataFrame(columns=data.columns).drop(columns=["artists_clean"])
                new_row.loc[0,row.index] = row
                new_row=new_row.fillna("1").astype(GET_SPOTIFY_DTYPES)
                if PROJECT_STATE=="cloud":
                    load_data_to_bq(new_row, GCP_PROJECT, BUCKET_NAME, 'raw_data', False)
                new_row['name'] = new_row['name'].str.lower()
                new_row['artists'] = new_row['artists'].str.lower()
                new_row = add_artists_clean(new_row)
                data = pd.concat([data, new_row], ignore_index=False, axis=0)

    return data
