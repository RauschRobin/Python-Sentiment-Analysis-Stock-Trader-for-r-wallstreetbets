# Python_Projekt
This is our python project from the Wahlfach Python aus Semester 4.

## Requirements for the Python Kernel
```
pip install praw==7.7.0
pip install twelvedata==1.2.11
pip install nltk==3.8.1
pip install pyyaml==6.0
pip install streamlit==1.22.0
pip install matplotlib==3.7.1
```
Bevor das Projekt zum ersten mal gestartet wird, muss einmal ```nltk.download('punkt')``` in einem zusätzlichen Python script(SETUP_install_nltk_punkt.py) ausgeführt werden.

## What does this nearly godlike code do?
This code checks the r/wallstreetbets subreddit daily and reads the top posts of the day. It then proceeds by buying or selling the stock the posts mention. To read and intrepret the posts, we implemented a sentiment analysis bot that uses machine learning. To train this bot we create a unique dataset that's specific to r/wallstreetbets. To buy, hold and sell the stocks, we created a handler that simulates these transactions with the real stock prices that we got from an stock market api at that exact time.

## What's the goal of this project?
Get rich fast & a good grade in the Wahlfach!
