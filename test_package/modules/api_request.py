import requests
import pandas as pd
from test_package.params import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Zyla API
def fetch_page(page, city, min_date, max_date):
    """
    Fetch a page of gigs from the zylab API
    """
    url = 'https://zylalabs.com/api/94/music+gigs+and+concerts+tracker+api/149/get+upcoming+concerts+by+location'

    headers = {
        'Authorization': F'Bearer {ZYLALAB_KEY}'
}
    params = {'name' : city, 'minDate' : min_date, 'maxDate' : max_date, 'page' : page}
    response = requests.request("GET", url, headers=headers, params=params).json()
    page_dict = response['data']
    return page_dict

def parse_data(page_dict):
    """
    Parse the data from the zylab API page dict lists
    """
    artist_list = []
    for i in page_dict:
        if i['@type'] == 'MusicEvent':
            artist_list.append(i['name'])
    return artist_list

def gather_gigs(city, min_date, max_date):
    """
    Gather all the gigs from the zylab API
    """
    page = 1
    artist_list = []
    gig_dict_list = []
    while True:
        page_dict = fetch_page(page, city, min_date, max_date)
        if len(page_dict) == 0:
            break
        artist_list.extend(parse_data(page_dict))
        gig_dict_list.extend(page_dict)
        page += 1
    return artist_list, gig_dict_list

# Bandsintown API
def bandsintown_request(artist_name, min_date, city='Lisboa'):
    """
    Get the bandsintown info for the artist
    """

    print('Getting bandsintown info...')

    params = {'date':'upcoming'}

    url = 'https://rest.bandsintown.com/artists/'
    response = requests.get(f'{url}{artist_name}/events?app_id={BANDSINTOWN_KEY}', params=params).json()

    gig_list = []
    try:
        for gig in response:
            if gig['venue']['city'] == city and gig['starts_at'] >= min_date:
                gig_list.append(gig)

        if city == 'Lisboa' and len(gig_list) == 0:

            city = 'Lisbon'

            for gig in response:
                if gig['venue']['city'] == city and gig['starts_at'] >= min_date:
                    gig_list.append(gig)

        ticket_link = gig_list[0]['url']
        longitude = gig_list[0]['venue']['longitude']
        latitude = gig_list[0]['venue']['latitude']

        print('Bandsintown info gathered! :)')
    except TypeError:
        print('Bandsintown info not found! :(')
        ticket_link = None
        longitude = None
        latitude = None
    return ticket_link, longitude, latitude


# Spotify API
def get_track_ids_by_artist(artist_name):
    tracks = []
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               ))
    data = sp.search(q=f"{artist_name}", type="track", limit=20)
    for item in data["tracks"]["items"]:
        artists = str([artist["name"]for artist in item.get("artists")])
        tracks.append({
            "id":item.get("id"),
            "name":item.get("name"),
            "artists":artists,
            })
    return pd.DataFrame(tracks)

def get_audio_features(tracks):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               ))
    data = sp.audio_features(tracks["id"])
    return pd.merge(tracks,pd.DataFrame(data),on="id").drop(columns=["type","uri","track_href","analysis_url"])

def get_spotify_df(artist_name):
    tracks = get_track_ids_by_artist(artist_name)
    audio_features = get_audio_features(tracks)
    return audio_features
