from sklearn.neighbors import NearestNeighbors
from test_package.modules.preprocessing import preprocess_numerical
from test_package.modules.PCA import pca

def fit_nn(data):

    song_knn = NearestNeighbors(n_neighbors=len(data)).fit(data)

    return song_knn

def init_model(data,
               matched_df):
    """
    Initialize the model and return the model object as well as the PCA'd data
    """

    print('Starting model initialization')


    preproc_num = preprocess_numerical(data)
    print('got to matched df preproc')
    preproc_matched_num = preprocess_numerical(matched_df)
    print('Got to pca!')
    data_pca, data_matched_pca = pca(preproc_num, preproc_matched_num)
    print('got to fit_nn')
    song_knn = fit_nn(data_matched_pca)

    print('Finished model initialization :)')

    return song_knn, data_pca
