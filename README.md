# Python_Projekt
This is our python project from the Wahlfach Python aus Semester 4.

## Requirements for the Python Kernel
```
pip install praw==7.7.0
pip install twelvedata==1.2.11
pip install nltk==3.8.1
pip install pyyaml==6.0
```

## What does this nearly godlike code do?
This code checks the r/wallstreetbets subreddit daily and reads the top posts of the day. It then proceeds by buying or selling the stock the posts mention. To read and intrepret the posts, we implemented a sentiment analysis bot that uses machine learning. To train this bot we create a unique dataset that's specific to r/wallstreetbets. To buy, hold and sell the stocks, we created a handler that simulates these transactions with the real stock prices that we got from an stock market api at that exact time.

## What's the goal of this project?
Get rich fast!

## Why did you code in python?
Because it's simple and we were forced by our Wahlfach Dozent! Please help!

Ein Call wird bei steigenden Kursen seines Basiswertes wertvoller, ein Put bei fallenden Kursen