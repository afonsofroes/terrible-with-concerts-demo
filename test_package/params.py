import os
from pathlib import Path

SPOTIFY_KEY = os.environ.get('SPOTIFY_KEY')
ZYLALAB_KEY = os.environ.get('ZYLALAB_KEY')
BANDSINTOWN_KEY = os.environ.get('BANDSINTOWN_KEY')

GET_SPOTIFY_DTYPES = {'id' : 'str',
                        'name' : 'str',
                        'album' : 'str',
                        'album_id' : 'str',
                        'artists' : 'str',
                        'artist_ids' : 'str',
                        'track_number' : 'int32',
                        'disc_number' : 'int32',
                        'explicit' : 'int32',
                        'danceability' : 'float32',
                        'energy' : 'float32',
                        'key' : 'int32',
                        'loudness' : 'float32',
                        'mode' : 'int32',
                        'speechiness' : 'float32',
                        'acousticness' : 'float32',
                        'instrumentalness' : 'float32',
                        'liveness' : 'float32',
                        'valence' : 'float32',
                        'tempo' : 'float32',
                        'duration_ms' : 'int32',
                        'time_signature' : 'int32',
                        'year' : 'int32',
                        'release_date' : 'str',
                        }

LOCAL_REGISTRY_PATH =os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")
DATA_PATH = Path(__file__).parent.parent.resolve().joinpath("raw_data","tracks_features.csv")
MODEL_PATH = Path(__file__).parent.resolve().joinpath("pca.pkl")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
BQ_DATASET = os.environ.get("BQ_DATASET")
GCP_PROJECT=os.environ.get("GCP_PROJECT")
SPOTIFY_CLIENT_ID=os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.environ.get("SPOTIFY_CLIENT_SECRET")

PROJECT_STATE=os.environ.get("PROJECT_STATE")
