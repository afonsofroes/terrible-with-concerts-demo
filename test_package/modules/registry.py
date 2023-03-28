import pickle
from colorama import Fore, Style
from test_package.params import *
from google.cloud import storage, bigquery
import pandas as pd

from pathlib import Path


def save_model(model) -> None:
    """
    Persist trained model locally on hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it on your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on mlflow instead of GCS (for unit 0703 only) --> unit 03 only
    """

    pickle.dump(model, open("pca.pkl","wb"))

    client = storage.Client(project=GCP_PROJECT)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('pca.pkl')
    # Upload the pickle file to the cloud
    blob.upload_from_filename('pca.pkl')

    return None

def load_model(cache_path:Path):

    if cache_path.is_file():

        pca_model = pickle.load(open(cache_path,'rb'))
    else:
        client = storage.Client(project=GCP_PROJECT)

        bucket = client.bucket(BUCKET_NAME)

        with open('pca.pkl', 'wb') as f:
            blob = bucket.get_blob('pca.pkl')
            blob.download_to_file(f)

        with open('pca.pkl', 'rb') as f:
            pca_model = pickle.load(f)

    return pca_model

def load_data_to_bq(data: pd.DataFrame,
              gcp_project:str,
              bq_dataset:str,
              table: str,
              truncate: bool) -> None:
    """
    - Save dataframe to bigquery
    - Empty the table beforehands if `truncate` is True, append otherwise.
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
    print(Fore.BLUE + f"\nSave data to bigquery {full_table_name}...:" + Style.RESET_ALL)

    # Load data to full_table_name
    # 🎯 Hint for "*** TypeError: expected bytes, int found":
    # BQ can only accept "str" columns starting with a letter or underscore column


    client = bigquery.Client(project=gcp_project)

    if truncate:
        client.delete_table(full_table_name,not_found_ok=True)
        write_mode = "WRITE_TRUNCATE"
    else:
        write_mode = "WRITE_APPEND"

    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)
    if type(data.columns[0]) != str:
        data.columns = "_" + data.columns.astype('str')
    job = client.load_table_from_dataframe(data,full_table_name, job_config=job_config)
    job.result()
