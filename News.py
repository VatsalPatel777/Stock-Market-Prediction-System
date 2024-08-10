from newsapi import NewsApiClient
import CONSTANTS
import pandas as pd

class News:
    def __init__(self) -> None:
        self.newsapi = NewsApiClient(api_key=CONSTANTS.news_api_key)
    
    def get_everything(self, query):
        news = self.newsapi.get_everything(q=query, language="en")
        final_news = []
        for elem in news['articles']:
            final_news.append(elem['description'])
        df = pd.DataFrame(final_news, columns=["text"])
        df["sentiment"] = ""
        df.to_csv("news.csv")
        return df

    def top_headlines(self, query):
        news = self.newsapi.get_top_headlines(q=query, category="business", language="en", country="in")
        final_news = []
        for elem in news['articles']:
            final_news.append(elem['description'])
        df = pd.DataFrame(final_news, columns=["text"])
        df["sentiment"] = ""
        return df   