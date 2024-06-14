from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import numpy as np


class Vectoriz:
    def __init__(self, options):
        self.method = options.get('method', 'word2vec')
        self.vectorizer = None
        self.model = None
        self._initialize_vectorizer(options)

    def _initialize_vectorizer(self, options):
        if self.method == 'word2vec':
            self._init_word2vec(options)
        elif self.method == 'tf-idf':
            self._init_tfidf()
        else:
            raise ValueError("Unsupported method. Choose 'word2vec' or 'tf-idf'.")

    def _init_word2vec(self, options):
        vector_size = options.get('vector_size', 200)
        window = options.get('window', 10)
        min_count = options.get('min_count', 5)
        sg = options.get('sg', 1)
        epochs = options.get('epochs', 20)
        self.vectorizer = lambda corpus: Word2Vec(corpus, vector_size=vector_size, window=window, min_count=min_count, sg=sg, epochs=epochs)

    def _init_tfidf(self):
        self.vectorizer = TfidfVectorizer()

    def fit(self, corpus):
        preprocessed_corpus = [simple_preprocess(doc) for doc in corpus]
        if self.method == 'word2vec':
            self.model = self.vectorizer(preprocessed_corpus)
            document_vectors = []
            for doc in preprocessed_corpus:
                words_vectors = [self.model.wv[word] for word in doc if word in self.model.wv]
                if words_vectors:
                    doc_vector = np.mean(words_vectors, axis=0)
                else:
                    doc_vector = np.zeros(self.model.vector_size)
                document_vectors.append(doc_vector)
            return np.array(document_vectors)
        elif self.method == 'tf-idf':
            vectors = self.vectorizer.fit_transform(corpus)
            return vectors.toarray()

    def get_points_name(self, vectors):
        if self.method == 'word2vec' and self.model is not None:
            text_corpus = []
            for vector in vectors:
                similar_words = self.model.wv.similar_by_vector(vector, topn=1)
                if similar_words:
                    similar_word = similar_words[0][0]
                    text_corpus.append(similar_word)
                else:
                    text_corpus.append("unknown")
            return text_corpus
        else:
            raise ValueError("Only supported for 'word2vec' method or model not fitted.")

    def check_model_quality(self, corpus):
        words_to_check = ['good', 'bad', 'user']
        for word in words_to_check:
            if word in self.model.wv:
                similar_words = self.model.wv.most_similar(word)
                print(f"Words similar to '{word}': {similar_words}")
            else:
                print(f"'{word}' not in vocabulary")

        # Analogy tasks
        analogies = [
            ('nice', 'awesome', 'good', 'best'),
            ('thanks', 'please', 'help', 'excuse'),
            ('write', 'draw', 'say', 'show')
        ]
        for a, b, c, expected in analogies:
            if all(word in self.model.wv for word in [a, b, c]):
                predicted = self.model.wv.most_similar(positive=[b, c], negative=[a], topn=1)[0][0]
                print(f"{a} is to {b} as {c} is to {expected}: Predicted: {predicted}")
            else:
                print(f"One of the words in analogy ({a}, {b}, {c}) not in vocabulary")

        # Vocabulary coverage
        preprocessed_corpus = [simple_preprocess(doc) for doc in corpus]
        vocab_coverage = sum(1 for doc in preprocessed_corpus for word in doc if word in self.model.wv)
        total_words = sum(len(doc) for doc in preprocessed_corpus)
        coverage_percentage = (vocab_coverage / total_words) * 100
        print(f"Vocabulary coverage: {coverage_percentage:.2f}%")