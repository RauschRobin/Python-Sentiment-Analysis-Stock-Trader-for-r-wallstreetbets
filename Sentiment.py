'''
This is the Sentiment class. A Instance of this class stores the sentiment of the sentiment analysis bot to a new reddit post. The sentiment consists of the sentiment which can be positive or negative and the accuracy between 0 and 1.
'''
class Sentiment:
    def __init__(self, sentiment, accuracy):
        '''
        This function is called when creating an instance of Sentiment. It sets the sentiment and accuracy.

        Parameters:
        sentiment: string
        accuracy: float

        Returns:
        Nothing
        '''
        self.sentiment = sentiment
        self.accuracy = accuracy