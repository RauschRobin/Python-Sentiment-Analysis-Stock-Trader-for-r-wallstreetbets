import json
import re
import nltk
from nltk.tokenize import word_tokenize

# Preprocess the text data
def preprocess_text(text):
    # Remove unwanted characters
    text = re.sub(r'[^\w\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    # Tokenize text into words
    words = word_tokenize(text)
    return words

# Define a feature extractor function
def extract_features(title_processed, gain_or_loss):
    features = {}
    for word in title_processed:
        features['contains({})'.format(word)] = True
    features['gain_or_loss'] = gain_or_loss
    return features

def main():
    # Load the dataset from the JSON file
    with open('sentiment_analysis_bot_dataset.json') as f:
        dataset = [json.loads(line) for line in f]

    # Preprocess the title column in the dataset
    for data in dataset:
        data['title_processed'] = preprocess_text(data['title'])

    # Extract features for each data point in the dataset
    featuresets = [(extract_features(data['title_processed'], data['gain_or_loss']), data['sentiment']) for data in dataset]

    # Split the dataset into a training set and a testing set
    split = int(0.7 * len(featuresets))
    train_set = featuresets[:split]
    test_set = featuresets[split:]

    # Train a Naive Bayes classifier
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # Test the classifier
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print('Accuracy based on the given dataset: {:.2f}%'.format(accuracy * 100))

    # Classify new data
    title = 'Yo dipshits! Sell GME. It sucks!'
    gain_or_loss = 'gain'
    title_processed = preprocess_text(title)
    features = extract_features(title_processed, gain_or_loss)
    sentiment = classifier.classify(features)
    print(sentiment)
    classifier.show_most_informative_features()

if __name__ == "__main__":
    main()
