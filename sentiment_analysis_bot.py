import json
import re
import nltk
import os
from nltk.tokenize import word_tokenize
from Sentiment import Sentiment

class SentimentAnalysisBot:
    def __init__(self):
        '''
        Initializes the sentiment analysis bot and trains it with the static dataset.

        Returns:
        None
        '''
        # name of dataset file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.data_file = os.path.join(dir_path, 'sentiment_analysis_bot_dataset.json')
        # loads dataset
        self.dataset = self.load_dataset()
        self.featuresets = self.extract_featuresets()

    def preprocess_text(self, text):
        '''
        Preprocesses the input text by removing unwanted characters, converting to lowercase and tokenizing the text into words.

        Parameters:
        text (str): The input text to be preprocessed.

        Returns:
        list: A list of preprocessed words.

        Possible Tests:
        Test for removing unwanted characters: This test would take a string with unwanted characters and check if the function is able to remove them successfully. Symbols such as '#', '@', and '*', as well as punctuation marks such as commas, periods, and exclamation marks. The test would assert that the resulting list of preprocessed words does not contain any unwanted characters.

        Test for converting text to lowercase: This test would take a string containing both uppercase and lowercase characters and check if the function is able to convert all characters to lowercase. The test would assert that the resulting list of preprocessed words only contains lowercase characters.

        Test for tokenizing text into words: This test would take a string containing multiple words and check if the function is able to tokenize the text into individual words. The test would assert that the resulting list of preprocessed words contains the same number of words as the input text and that each word is correctly separated and stored in the list.
        '''
        # Remove unwanted characters
        text = re.sub(r'[^\w\s]', '', text)
        # Convert text to lowercase
        text = text.lower()
        # Tokenize text into words
        words = word_tokenize(text)
        return words

    def load_dataset(self):
        '''
        Loads the dataset from the JSON file and preprocesses the title column in the dataset.

        Returns:
        list: A list of dictionaries, where each dictionary represents a data point in the dataset.

        Possible Tests:
        The first test would check if the function is able to load the dataset from the JSON file without any errors. The test could involve checking the length of the returned list of dictionaries to ensure that it matches the expected number of data points in the dataset.

        Test for preprocessing title column: This test would check if the function is able to preprocess the 'title' column in the dataset using the 'preprocess_text' function without any errors. The test could involve checking that the resulting 'title_processed' column in each dictionary contains a list of preprocessed words that match the expected output of the 'preprocess_text' function.

        Test for handling invalid data: This test would check if the function can handle invalid data in the dataset, such as missing or malformed 'title' fields. The test could involve passing a dataset with missing or invalid 'title' fields and checking that the function raises an appropriate error or handles the invalid data gracefully by skipping over those data points.
        '''
        # Load the dataset from the JSON file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(self.data_file, 'r', encoding="utf-8") as f:
            dataset = json.load(f)
        # Preprocess the title column in the dataset
        for data in dataset:
            data['title_processed'] = self.preprocess_text(data['title'])
        return dataset

    def extract_featuresets(self):
        '''
        Extracts features for each data point in the dataset.

        Returns:
        list: A list of tuples, where each tuple contains a dictionary of features and a sentiment label for a single data point in the dataset.

        Possible Tests:
        A test would check if the function is able to extract features for each data point in the dataset without any errors. The test could involve checking the length of the returned list of tuples to ensure that it matches the expected number of data points in the dataset.

        Test for feature dictionary: This test would check if the function is able to generate a dictionary of features for each data point in the dataset without any errors. The test could involve checking that the resulting feature dictionary for a single data point contains the expected keys and values.
        '''
        # Extract features for each data point in the dataset
        featuresets = [(self.extract_features(data['title_processed']), data['sentiment']) for data in self.dataset]
        return featuresets

    def extract_features(self, title_processed):
        '''
        Extracts features for a single data point in the dataset, given its preprocessed title.

        Parameters:
        title_processed (list): A list of preprocessed words representing the title of a data point in the dataset.

        Returns:
        dict: A dictionary of features, where each key is a string of the form "contains({word})", and each value is True or False, depending on whether the word is present in the title or not.

        Possible Tests:
        This test would check if the function is able to generate feature keys in the expected format for a given set of preprocessed words without any errors. The test could involve passing a preprocessed title with a known set of words and checking that the resulting feature keys match the expected format.

        Another test would check if the function is able to handle empty or invalid input without any errors. The test could involve passing an empty list or a list with invalid data types as the input 'title_processed' and checking that the function raises an appropriate error or handles the invalid data gracefully by returning an empty feature dictionary.
        '''
        # Splits the sentence into different words
        features = {}
        for word in title_processed:
            features['contains({})'.format(word)] = True
        return features


    def train_classifier(self):
        '''
        Trains a Naive Bayes classifier on the training set of the dataset.

        Returns:
        tuple: A tuple of the form (classifier, test_set), where classifier is a trained NaiveBayesClassifier object, and test_set is a list of tuples, where each tuple contains a dictionary of features and a sentiment label for a single data point in the testing set of the dataset.

        Possible Tests:
        Test for training set size: This test would check if the function is able to correctly split the dataset into a training set and a testing set without any errors. The test could involve checking the length of the resulting training and testing sets to ensure that they match the expected sizes based on the split ratio.

        Test for classifier training: This test would check if the function is able to train a Naive Bayes classifier on the training set without any errors. The test could involve checking that the resulting classifier object is not None or empty and that it has been trained on the expected number of data points.

        Test for testing set: This test would check if the function is able to correctly generate the testing set of tuples with feature dictionaries and sentiment labels for each data point in the testing set without any errors. The test could involve checking the length of the resulting test set to ensure that it matches the expected size based on the split ratio, and also checking that each tuple in the test set contains the expected keys and values for the feature dictionary and sentiment label.
        '''
        # Split the dataset into a training set and a testing set
        split = int(0.7 * len(self.featuresets))
        train_set = self.featuresets[:split]
        test_set = self.featuresets[split:]

        # Train a Naive Bayes classifier
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier, test_set

    def test_classifier(self, classifier, test_set):
        '''
        Tests the classifier on its accuracy. It does that by dividing the dataset in two and using the bigger part to train the classifier and the smaller part to test its accuracy. 

        Returns:
        None

        Possible Tests:
        None
        '''
        # Test the classifier based on the remaining 30% of the dataset
        accuracy = nltk.classify.accuracy(classifier, test_set)
        #print('Accuracy based on the given dataset: {:.2f}%'.format(accuracy * 100))

    def classify_sentiment(self, title):
        '''
        Tries to classify the sentiment using the given title

        Returns:
        the sentiment of the classifier on a given title

        Possible Tests:
        Test for sentiment classification: This test would check if the function is able to correctly classify the sentiment of a given title using the trained Naive Bayes classifier. The test could involve providing a sample title that is known to have a specific sentiment (e.g. positive or negative) and checking if the function returns the correct sentiment label.

        Test for informative features: This test could involve calling the function self.classifier.show_most_informative_features() and checking if it returns the expected number of informative features for the trained classifier. This could help to verify that the classifier has been trained properly and is able to identify the most important words in determining the sentiment of a given title.
        '''
        # Preprocesses and splits the given post, then rates the sentiment
        title_processed = self.preprocess_text(title)
        features = self.extract_features(title_processed)
        sentiment = self.classifier.classify(features)
        accuracy = self.classifier.prob_classify(features).prob(self.classifier.prob_classify(features).max())
        SentimentAboutStock = Sentiment(sentiment, accuracy)
        # Why and how does the bot guess the sentiment in the way it did? --> Displays most important words:
        # self.classifier.show_most_informative_features()
        return SentimentAboutStock

    def run(self, title):
        '''
        Runs the classifier on a given title.

        Params:
        title: string

        Returns:
        The sentiment guessed by the classifier

        Possible Tests:
        Test the accuracy of the classifier by using an obvious title. The sentiment of the title should be clear. Assert the sentiment that function call.
        '''
        self.classifier, test_set = self.train_classifier()
        self.test_classifier(self.classifier, test_set)
        return self.classify_sentiment(title)
    