''' 
This file needs to be executed before running the main.py. It's responsible for downloading the "punkt" tokenizer package. The "punkt" tokenizer is a pre-trained model for splitting raw text into sentences and words. This only needs to be executed once!
'''
import nltk

nltk.download('punkt')