from newsapi import NewsApiClient
from .CONSTANTS import news_api_key
import pandas as pd
import http.client, urllib.parse


class News:
    def __init__(self) -> None:
        """Initializes NewsAPI client with API Keys."""
        self.newsapi = NewsApiClient(api_key=news_api_key)

    # def getNews(self, query):
    #     conn = http.client.HTTPConnection("api.marketaux.com")
    #     params = urllib.parse.urlencode(
    #         {
    #             "api_token": marketaux_api_token,
    #             "symbols": f"TSLA",
    #             "countries": "in"
    #         }
    #     )
    #     conn.request("GET", "/v1/news/all?{}".format(params))

    #     res = conn.getresponse()
    #     data = res.read()
    #     print(data.decode("utf-8"))

    def get_everything(self, query: str) -> pd.DataFrame:
        """
        Fetches everything related to the given query.\n
        Args:
            query (str): String related to the information to be fetched.
        Returns:
            pandas.DataFrame: Returns a pandas DataFrame with headlines etc. relevant to the query
        """
        news = self.newsapi.get_everything(q=query, language="en")
        final_news = []
        for elem in news['articles']:
            final_news.append(elem['description'])
        df = pd.DataFrame(final_news, columns=["text"])
        df["sentiment"] = ""
        return df

    def top_headlines(self, query):
        """
        Fetches top headlines related to the given query.\n
        Args:
            query (str): String related to the information to be fetched.
        Returns:
            pandas.DataFrame: Returns a pandas DataFrame with top headlines relevant to the query
        """

        news = self.newsapi.get_top_headlines(q=query, category="business", language="en", country="in")
        final_news = []
        for elem in news['articles']:
            final_news.append(elem['description'])
        df = pd.DataFrame(final_news, columns=["text"])
        df["sentiment"] = ""
        return df

