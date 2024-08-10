import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from News import News
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class SentimentAnalyzer:
    def __init__(self) -> None:
        new_words = {
            'flat': 0,
            "fell": -100,
            "red": -75,
            "green": 50,
            "level": 0,
            "gap up": 20,
            "gap down":-20,
            "gain": 100,
            "rise": 100,
            "lower": -50,
            "jump": 50,
            "rally": 100, 
            "winner": 50,
            "bullish": 100,
            "bearish": -100
        }
        
        self.analyzer = SentimentIntensityAnalyzer()
        self.analyzer.lexicon.update(new_words)
        
        self.News = News()

    def getNews(self, query):
        self.news = self.News.get_everything(query)
        # self.news = pd.read_csv("out.csv")

    def preprocessText(self, text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        processed_text = ' '.join(lemmatized_tokens)
        return processed_text
    
    def getSentiments(self):
        self.getNews("INFY")
        self.news = self.news.filter(items=["text"])
        scores = self.news["text"].apply(self.analyzer.polarity_scores)
        scores_df = pd.DataFrame.from_records(scores)
        self.news = self.news.join(scores_df)
        idx = 0
        self.news["compound"] = self.news["compound"].apply(lambda x: 1 if x > 0.2 else (-1 if x < -0.2 else 0))
    
    def plotSentimentAnalysis(self):
        self.getSentiments()
        count_0 = 0
        count_1 = 0
        count = 0
        for score in self.news['compound']:
            if score == 0:
                count_0 += 1
            elif score == 1:
                count_1 += 1
            else:
                count +=1
        
        y = [count_0, count_1, count]
        myLabels = [f"0:{count_0}", f"1:{count_1}", f"-1:{count}"]
        colors = ["#FFFF00", "#00FF00", "#FF0000"]
        plt.pie(y, labels=myLabels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
        centre_circle = plt.Circle((0,0),0.60,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        # ax1.axis('equal')  
        plt.show()


    
s = SentimentAnalyzer()    
s.plotSentimentAnalysis()