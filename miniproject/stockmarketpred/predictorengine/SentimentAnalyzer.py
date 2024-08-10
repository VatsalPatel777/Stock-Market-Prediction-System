import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from .News import News
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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
            "bearish": -100,
            "plunge": -100
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
        self.getNews("Sensex")
        self.news = self.news.filter(items=["text"])
        scores = self.news["text"].apply(self.analyzer.polarity_scores)
        scores_df = pd.DataFrame.from_records(scores)
        self.news = self.news.join(scores_df)
        idx = 0
        self.news["compound"] = self.news["compound"].apply(lambda x: 1 if x > 0.4 else (-1 if x < -0.4 else 0))
        # print(self.news)
        # self.news.to_csv("out.csv")
    
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
                count += 1
        y = [count_0, count_1, count]
        myLabels = [f"Neutral: {count_0}", f"Bullish: {count_1}", f"Bearish: {count}"]
        colors = ["#F5CB42", "#00FF00", "#FF0000"]
        fig = px.pie(values=y, names=myLabels, title="Sentiment Analysis", color_discrete_sequence=colors)

        if(max(count_0, count_1, count) == count_0):
            sentiment = "Neutral"
        elif(max(count_0, count_1, count) == count_1):
            sentiment = "Bullish"
        else:
            sentiment = "Bearish"
        return fig, sentiment
    
s = SentimentAnalyzer()    
s.plotSentimentAnalysis()