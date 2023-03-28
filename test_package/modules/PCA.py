from sklearn.decomposition import PCA


def init_pca(preproc_num):
    '''
    Initialize the PCA model and return the model object as well as the PCA'd data
    '''
    pca = PCA(n_components=5)
    data_pca = pca.fit_transform(preproc_num)

    return data_pca, pca

def matched_data_pca(preproc_num, data_matched):
    '''
    Return the PCA'd data for the matched data
    '''

    _, pca_model = init_pca(preproc_num)

    data_matched_pca = pca_model.transform(data_matched)

    return data_matched_pca


def pca(preproc_num, data_matched):
    print('Starting PCA')
    pca = PCA(n_components=5)
    data_pca = pca.fit_transform(preproc_num)
    print("Managed to fit the PCA model")
    data_matched_pca = pca.transform(data_matched)
    print("Managed to transform the matched data")

    print('Finished PCA :)')

    return data_pca, data_matched_pca
