from sklearn.compose import make_column_transformer
from sklearn.preprocessing import RobustScaler
import pandas as pd

'''
This is an adaptation of Pedro's original preprocessing pipeline.
'''

def preprocess_data(data):
    def preproc_pipeline():
        features_num = [
                "danceability",
                "energy",
                "acousticness",
                "instrumentalness",
                "valence",
                "tempo",
                "duration_ms",
                "loudness",
                "speechiness",
                "liveness"
                ]

        preproc_pipe = make_column_transformer(
            (RobustScaler(),features_num),
            remainder="passthrough"
            )

        return preproc_pipe

    pipeline = preproc_pipeline()

    df_preprocessed = pipeline.fit_transform(data)

    df_preprocessed = pd.DataFrame(df_preprocessed)

    return df_preprocessed

def preprocess_numerical(data):
    data_num = data.select_dtypes(exclude = ['object']).drop(columns = ['track_number', 'disc_number', 'key', 'year', 'explicit'])
    print('Select successful, doing preprocessing')
    proc_num = preprocess_data(data_num)

    return proc_num
