import json
import re
import nltk
from nltk.tokenize import word_tokenize

class SentimentAnalysisBot:
    def __init__(self):
        nltk.download("punkt")
        self.data_file = "sentiment_analysis_bot_dataset.json"
        self.dataset = self.load_dataset()
        self.featuresets = self.extract_featuresets()

    def preprocess_text(self, text):
        # Remove unwanted characters
        text = re.sub(r'[^\w\s]', '', text)
        # Convert text to lowercase
        text = text.lower()
        # Tokenize text into words
        words = word_tokenize(text)
        return words

    def load_dataset(self):
        # Load the dataset from the JSON file
        with open(self.data_file) as f:
            dataset = [json.loads(line) for line in f]
        # Preprocess the title column in the dataset
        for data in dataset:
            data['title_processed'] = self.preprocess_text(data['title'])
        return dataset

    def extract_features(self, title_processed, gain_or_loss):
        #Splits the sentence into different words
        features = {}
        for word in title_processed:
            features['contains({})'.format(word)] = True
        features['gain_or_loss'] = gain_or_loss
        return features

    def extract_featuresets(self):
        # Extract features for each data point in the dataset
        featuresets = [(self.extract_features(data['title_processed'], data['gain_or_loss']), data['sentiment']) for data in self.dataset]
        return featuresets

    def train_classifier(self):
        # Split the dataset into a training set and a testing set
        split = int(0.7 * len(self.featuresets))
        train_set = self.featuresets[:split]
        test_set = self.featuresets[split:]

        # Train a Naive Bayes classifier
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier, test_set

    def test_classifier(self, classifier, test_set):
        # Test the classifier based on the remaining 30% of the dataset
        accuracy = nltk.classify.accuracy(classifier, test_set)
        print('Accuracy based on the given dataset: {:.2f}%'.format(accuracy * 100))

    def classify_sentiment(self, title, gain_or_loss):
        #preprocesses, splits and then rates the given post
        title_processed = self.preprocess_text(title)
        features = self.extract_features(title_processed, gain_or_loss)
        sentiment = self.classifier.classify(features)
        return sentiment
        #Why and how does the bot guess the sentiment in the way it did? --> Show most important words
        #self.classifier.show_most_informative_features()

    def run(self, title, gain_or_loss):
        # Reloads and tests the sentiment bot and then calls classify_sentiment with the given post
        # Retrain and test can be removed, i think?
        self.classifier, test_set = self.train_classifier()
        self.test_classifier(self.classifier, test_set)
        return self.classify_sentiment(title, gain_or_loss)


"""
______________________ PACKAGES TO INSTALL ____________________________
pip install nltk

 _____________________ EXAMPLE USAGE: ____________________________
def main():
    title = 'Yo dipshits! Sell GME. It sucks!'
    gain_or_loss = 'gain'

    bot = SentimentAnalysisBot()
    bot.run(title, gain_or_loss)

if __name__ == "__main__":
    main()"""
