import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import keras
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' 

class Prediction:
    def makePredictions(self, name):
        stock = yf.download(tickers=name, period="10y")
        df = stock
        data = df.filter(['Adj Close'])
        dataset = data.values
        training_data_len = int(np.ceil( len(dataset) * .95 ))
        scaler = MinMaxScaler(feature_range=(0,1))
        
        self.scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)
        training_data_len = int(np.ceil( len(dataset) * .95 ))

        train_data = scaled_data[0:int(training_data_len), :]

        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = keras.models.load_model("StockMarketPredictor.h5")

        test_data = scaled_data[training_data_len - 60: , :]

        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])

        x_test = np.array(x_test)

        # Reshape the data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

        # Get the models predicted price values 
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        # Get the root mean squared error (RMSE)
        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
        # print(rmse)

        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions
        # Visualize the data
        train_df = pd.DataFrame({'Date': train.index, 'Close': train['Adj Close']})
        train_df = train_df.rename(columns={'Close': 'Train'})

        # Create a DataFrame from the validation data and predictions
        valid_df = pd.DataFrame({'Date': valid.index, 'Close': valid['Adj Close']})
        valid_df['Predictions'] = np.squeeze(predictions)  # Convert predictions to 1D
        valid_df = valid_df.rename(columns={'Close': 'Val'})

        # Concatenate the training and validation DataFrames
        data = pd.concat([train_df, valid_df['Val'], valid_df['Predictions']], axis=1)

        # Create a line plot using Plotly Express
        fig = px.line(x=train_df["Date"][1000:], y=train_df["Train"][1000:],title='Stock Price Prediction')
        fig.add_scatter(x=valid_df["Date"], y=valid_df["Val"], mode='lines', name='Train' , line=dict(color='#636EFA'))
        fig.add_scatter(x=valid_df["Date"], y=valid_df["Predictions"], mode='lines', name='Test', line=dict(color='red'))

        fig.update_traces(line={'width': 2})
        # Customize the plot
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Close Price INR',
            font=dict(size=18),
            legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01)
        )

        today = datetime.today().date()

        last_60_days = dataset[training_data_len:]

        scaler = MinMaxScaler(feature_range=(0, 1))
        last_60_days_scaled = scaler.fit_transform(last_60_days.reshape(-1, 1))

        x_test = []
        for i in range(60, len(last_60_days_scaled) + 1):
            x_test.append(last_60_days_scaled[i - 60:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        prediction_dates = []
        start_date = today
        for i in range(len(predictions)):
            prediction_date = start_date + timedelta(days=i)
            prediction_dates.append(prediction_date)

        predictions = predictions+(dataset[-1] - predictions[0][0])
        predictions_df = pd.DataFrame({'Date': prediction_dates, 'Close': np.squeeze(predictions)})
        predictions_df = predictions_df.set_index('Date')
    
        fig.add_scatter(x=predictions_df.index, y=predictions_df['Close'], mode='lines', name='Predictions', line=dict(color='Orange'))

        return fig
#-----------------------------------------------------------------------------------------
        

    def plotMA(self, name: str,period: int, clr: str):
        stock = yf.download(tickers=name, period="10y")
        values = stock["Close"].rolling(period).mean()
        fig = px.line(values[1000:], title=f"{period}-Day Moving Average", labels={"y": "Price", "x": "Day"})
        fig.update_layout(showlegend=False)

        return fig
    
    def plotMAinOne(self, name: str):
        stock = yf.download(tickers=name, period="10y")
        period = [10, 20, 50]
        ma = []
        for p in period:
            ma.append(stock["Close"].rolling(p).mean())
        # print(ma)
        dict = {
            "10-Day Moving Average": ma[0],
            "20-Day Moving Average": ma[1],
            "50-Day Moving Average": ma[2]
        }

        fig = px.line(y=ma[0][1000:], title=f"Superimposed Moving Average", labels={"y": "Price", "x": "Day"})
        fig.add_scatter(y=ma[1][1000:], mode='lines')
        fig.add_scatter(y=ma[2][1000:], mode='lines')
        fig.update_layout(showlegend=False)
        # print(stock.index)
        return fig

# p.plotDailyReturns()

