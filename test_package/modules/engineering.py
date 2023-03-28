import pandas as pd
from test_package.modules.api_request import gather_gigs

def add_artists_clean(data: pd.DataFrame):
    assert 'artists' in data.columns, "data frame doesnt have artists column"

    data['artists_clean'] = data['artists'].str.strip('[]').str.strip("'")
    data['artists_clean'] = data['artists_clean'].str.split("', '")
    return data

def add_matched_artists(data: pd.DataFrame,
                        artist_list: list):
    if 'artists_clean' not in data.columns:
        raise SystemExit("data frame doesnt have artists_clean column. See add_artists_clean")

    matched_i_list = []

    for artist in artist_list:
        song_i_list = data.index[data['artists_clean'].apply(lambda x: artist in x)]
        for song_i in song_i_list:
            matched_i_list.append(song_i)

    data = data.iloc[matched_i_list]

    data['matched_artist'] = [[artist for artist in artists if artist in artist_list]
                                        for artists in data['artists_clean']]
    return data

def generate_matched_df(data: pd.DataFrame,
                        city: str,
                        min_date: str,
                        max_date: str):
    """
    Generate a dataframe with only the songs that match the artist
    """
    print('Generating matched dataframe...')

    artist_list, gigs_dict = gather_gigs(city, min_date, max_date)

    artist_list_lower = [artist.lower() for artist in artist_list]

    data_clean_artists = add_artists_clean(data)

    matched_df = add_matched_artists(data_clean_artists, artist_list_lower)

    print('Matched dataframe generated! :)')

    return matched_df, artist_list, gigs_dict
