import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Additional stopwords specific to YouTube comments and markdown language
youtube_ml_stopwords = ['br', 'quot', 'http', 'https', 'amp', 'html']

# Additional stopwords in a more chat-style language
sprek_language_stop_words = ['u', 'xd', 'ur']

# Combine NLTK's English stopwords with custom stopwords
stop_words = set(stopwords.words("english") + youtube_ml_stopwords + sprek_language_stop_words)
lemmatizer = WordNetLemmatizer()


# options:
# alpha - delete spesical characters
# stop words - delte useles words (on , in , you)
# lemmatizer - words to base simple form


class TextProcess:
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.alpha = options.get('alpha', False)
        self.stop_word = options.get('stop_words', False)
        self.lemmatize = options.get('lemmatizer', False)
        if self.lemmatize:
            self.lemmatizer = WordNetLemmatizer()
        else:
            self.lemmatizer = None

    def fit(self, text):
        tokens = word_tokenize(text.lower())
        if self.alpha:
            tokens = [word for word in tokens if word.isalpha()]
        if self.stop_word:
            tokens = [word for word in tokens if word not in stop_words]
        if self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens]

        tokens = [word for word in tokens if word] # delete empty
        preprocessed_text = ' '.join(tokens)
        return preprocessed_text
