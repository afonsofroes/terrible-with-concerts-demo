from test_package.modules.preprocessing import preprocess_numerical
from test_package.modules.nn_model import fit_nn
from test_package.modules.engineering import generate_matched_df, add_artists_clean
from test_package.modules.sanitizing import sanitize_zasham
from test_package.modules.add_from_spotify import get_new_songs, fill_missing_artists
from test_package.modules.cloud import get_model, get_data
from test_package.modules.final_processing import final_processing
from test_package.params import *
import pandas as pd
import re

def main(min_date: str,
         max_date: str,
         city: str,
         artist_name: str,
         song_name: str):

    query = f"""
            SELECT *
            FROM {GCP_PROJECT}.{BQ_DATASET}.tracks_features
            """

    data = get_data(GCP_PROJECT, query, DATA_PATH)
    data_preprocessed = preprocess_numerical(data)

    pca_model = get_model(MODEL_PATH)
    print("Got PCA Model")


    # make everything case insensitive
    data['name'] = data['name'].str.lower()
    data['artists'] = data['artists'].str.lower()
    artist_name = artist_name.lower()
    song_name = song_name.lower()

    # add a column with the cleaned artists
    print("Adding artists_clean")
    data = add_artists_clean(data)
    print("Finding song in df")
    song_index = None
    try:
        song_index = data.index[(data.name == song_name ) & (data.artists.str.find(sanitize_zasham(artist_name)) != -1)][0] # find the index of the song in the original dataframe from the zasham'd song
    except IndexError:
        print('Could not find song, doing black magic...')
        data = get_new_songs(data, artist_name, song_name) # if the song is not in the original dataframe, get it from spotify
        song_index = data.index[(data.name == song_name ) & (data.artists.str.find(sanitize_zasham(artist_name)) != -1)][0]
    # generate a dataframe with only the songs that match the artist found
    matched_df, artist_list, gigs_dict = generate_matched_df(data,
                                                             city,
                                                             min_date,
                                                             max_date)

    if PROJECT_STATE == "update":
        print("Updating the dataframe with the new songs...")
        data = fill_missing_artists(data, artist_list) # fill the missing artists in the original dataframe
        data.drop(columns=['artists_clean']).to_csv('new_data.csv', index=False) # save the updated dataframe

    data_preprocessed = preprocess_numerical(data)
    data_pca = pca_model.transform(data_preprocessed)
    print("Transformed Data")
    song_knn = fit_nn(data_pca)
    print("Fitted NN")

    matched_df = matched_df.reset_index(drop=True)

    nn_distance = pd.Series(song_knn.kneighbors(data_pca[song_index].reshape(1,-1),
                                                return_distance=True)[0][0]) # find the distance to the all nn points
    old_index = pd.Series(song_knn.kneighbors(data_pca[song_index].reshape(1,-1),
                                              return_distance=True)[1][0]) # find the relative index of the all nn points

    nn_distance_df = pd.concat([nn_distance, old_index], axis=1) # create a dataframe with the distance and the relative index
    nn_distance_df = nn_distance_df.set_index(1) # set the relative index as the index of the dataframe
    suggestion_dicts = final_processing(matched_df, nn_distance_df, gigs_dict, min_date, city)
    print(suggestion_dicts)
    return suggestion_dicts


### AF added until here
if __name__ == '__main__':
    main("2023-03-01", "2023-03-31", "Lisboa", artist_name = "avicii", song_name = "wake me up")
