from modules.nn_model import init_model
from modules.engineering import generate_matched_df, add_artists_clean
from modules.sanitizing import sanitize_zasham
from modules.add_from_spotify import get_new_songs, fill_missing_artists
from modules.final_processing import final_processing
from params import *
import pandas as pd

'''
This module was used to test the whole program locally. Changes were eventually
made to the main.py file to make it work on the cloud, and to make code block
more condensed.
'''

def find_gig(artist_name,
             song_name,
             city='Lisboa',
             min_date='2023-03-01',
             max_date='2023-03-31'
            ):
    """
    Find a gig based on a shazam'd song
    """
    print('Loading data...')
    data = pd.read_csv('./raw_data/tracks_features.csv')
    print('Data loaded! :)')

    data['name'] = data['name'].str.lower() # make every input case insensitive
    data['artists'] = data['artists'].str.lower()
    artist_name = artist_name.lower()
    song_name = song_name.lower()

    data = add_artists_clean(data) # add a column with the cleaned artists

    song_index = None
    try:
        song_index = data.index[(data.name == song_name ) & (data.artists.str.find(sanitize_zasham(artist_name)) != -1)][0] # find the index of the song in the original dataframe from the zasham'd song
    except IndexError:
        print('Could not find song, doing black magic...')
        data = get_new_songs(data, artist_name, song_name) # if the song is not in the original dataframe, get it from spotify
        song_index = data.index[(data.name == song_name ) & (data.artists.str.find(sanitize_zasham(artist_name)) != -1)][0]

    matched_df, artist_list, gigs_dict = generate_matched_df(data, city, min_date, max_date) # generate a dataframe with only the songs that match the artist found
    print('Looking for missing artists...')
    #data = fill_missing_artists(data, artist_list) # fill the missing artists in the original dataframe
    print('Added some new songs! :)')

    print('Reseting index...')
    matched_df = matched_df.reset_index(drop=True)
    print('Done! :)')

    song_knn, data_pca = init_model(data, matched_df) # initialize the model and apply PCA

    print('Found song index! :)')
    print(data_pca[song_index].shape)
    print(data_pca[song_index])
    nn_distance = pd.Series(song_knn.kneighbors(data_pca[song_index].reshape(1,-1),
                                                return_distance=True)[0][0]) # find the distance to the all nn points
    old_index = pd.Series(song_knn.kneighbors(data_pca[song_index].reshape(1,-1),
                                              return_distance=True)[1][0]) # find the relative index of the all nn points
    print('Got diatnces! :)')
    nn_distance_df = pd.concat([nn_distance, old_index],axis=1) # create a dataframe with the distance and the relative index
    nn_distance_df = nn_distance_df.set_index(1) # set the relative index as the index of the dataframe
    print('Got the distance df! :)')

    suggestion_dicts = final_processing(matched_df, nn_distance_df, gigs_dict, min_date, city)

    return suggestion_dicts

if __name__ == '__main__':
    find_gig(artist_name = "buddy", song_name = "she think")


    # Don Campbell - The Reach in Lisbon returned an artist that doesn't exist in the bit API
    # multiple artists needs work
    # Vasco suggest:  blank if you wanna use your IP, otherwise IP check for lcoation
    # She Think	- ['Buddy', 'Kent Jamz']
