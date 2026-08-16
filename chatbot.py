import json
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Ensure NLTK punkt tokenizer is available (download only if missing)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class ChatBot:
    def __init__(self, intent_file):
        self.intent_file = intent_file
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self.intents = {}
        self._load_data()
        self._train_model()

    def _load_data(self):
        with open(self.intent_file, 'r') as f:
            data = json.load(f)
        self.X = []
        self.y = []
        for item in data:
            intent = item['intent']
            self.intents[intent] = item['responses']
            for pattern in item['patterns']:
                self.X.append(pattern)
                self.y.append(intent)

    def _train_model(self):
        self.X_vectorized = self.vectorizer.fit_transform(self.X)
        self.model.fit(self.X_vectorized, self.y)

    def get_response(self, user_input):
        input_vec = self.vectorizer.transform([user_input])
        intent = self.model.predict(input_vec)[0]
        return random.choice(self.intents.get(intent, ["Sorry, I don't understand that."]))
