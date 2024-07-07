YOUTUBE_API = 'AIzaSyB9oMKtQWNyGNuhKLb4ES_PmV29Axypq-I'

TEXTPROCES_DEFAULT = {
    'alpha': True,
    'stop-words': True,
    'lemmatizer': True
}

VECTOR_DEFAULT = {
    'method': 'word2vec',
    'vector_size': 150,
    'window': 10,
    'min_count': 5,
    'sg': 1
}

CLUSTER_DEFAULT = {
    'method': 'k-means',
    'num_clusters': 15
}