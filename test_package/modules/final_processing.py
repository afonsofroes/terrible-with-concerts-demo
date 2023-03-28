import pandas as pd
import re
from test_package.modules.api_request import bandsintown_request

def final_processing(matched_df, nn_distance_df, gigs_dict, min_date, city):
    final_df = matched_df.join(nn_distance_df) # set up df containing the matched songs and the distance to the nn points
    final_df = final_df.rename(columns={0:'nn_distance'})
    final_df['matched_artist'] = final_df['matched_artist'].str[0]
    artist_distance = pd.DataFrame(final_df.nn_distance.groupby(final_df.matched_artist).mean().sort_values())
    best_matched_artists = artist_distance.index[:5]


    suggestion_dicts = []


    gigs_df = pd.DataFrame(gigs_dict)

    get_name_regex =  r'\d+\s+([\w\s]+)at\s+([\w\s]+)'
    get_date_regex = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'

    for artist in best_matched_artists:
        suggested_gig = gigs_df[gigs_df['name'] == artist.title().strip("'")]
        try:
            suggested_gig_description = suggested_gig['description'].to_string()
            suggested_gig_startDate = suggested_gig['startDate'].to_string()
            suggested_gig_name = re.search(get_name_regex, suggested_gig_description).group(1).strip() # select the suggested gig name
            suggested_gig_date = re.search(get_date_regex, suggested_gig_startDate).group(0) # select the suggested gig date
        except AttributeError:
            suggested_gig_name = None
            suggested_gig_date = None
        try:
            url, latitude, longitude = bandsintown_request(artist, min_date, city)
        except IndexError:
            url = None
            latitude = None
            longitude = None


        output_dict = {'best_matched_artist': artist.title(),
                        'suggested_gig_name': suggested_gig_name,
                        'suggested_gig_date': suggested_gig_date,
                        'ticket_url': url,
                        'latitude': latitude,
                        'longitude': longitude}

        suggestion_dicts.append(output_dict)


    return suggestion_dicts
