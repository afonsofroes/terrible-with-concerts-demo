import pandas as pd
from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path
from test_package.modules.registry import load_model
from test_package.params import *
import pickle


def get_data(gcp_project:str,
                 query:str,
                 cache_path:Path) -> pd.DataFrame:
    """
    Retrieve `query` data from Big Query, or from `cache_path` if file exists.
    Store at `cache_path` if retrieved from Big Query for future re-use.
    """
    if PROJECT_STATE=="development" or PROJECT_STATE=="update":
        print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)
        df = pd.read_csv(cache_path)

    else:
        print(Fore.BLUE + "\nLoad data from Querying Big Query server..." + Style.RESET_ALL)
        client = bigquery.Client(project=gcp_project)
        query_job = client.query(query)
        result = query_job.result()
        df = result.to_dataframe()

        # Store as CSV if BQ query returned at least one valid line
        if df.shape[0] > 1:
            df.to_csv(cache_path, index=False)

    print(f"✅ Data loaded, with shape {df.shape}")

    return df

def get_model(cache_path:Path):
    if cache_path.is_file():
        print(Fore.BLUE + "\nLoading the model..." + Style.RESET_ALL)
        pca = pickle.load(open(cache_path,'rb'))
    else:
        print(Fore.BLUE + "\nFetching the model..." + Style.RESET_ALL)
        pca = load_model(MODEL_PATH)

    return pca
