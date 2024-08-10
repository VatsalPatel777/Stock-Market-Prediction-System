import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import keras
import os
from datetime import datetime, timedelta
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' 

stock = yf.download(tickers="RELIANCE.NS", period="10y")
df = stock
data = df.filter(['Adj Close'])
dataset = data.values
training_data_len = int(np.ceil( len(dataset) * .95 ))
scaler = MinMaxScaler(feature_range=(0,1))

# self.scaler = MinMaxScaler(feature_range=(0,1))
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
print(test_data.shape)
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])
x_test = np.array(x_test)
# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))
# print(x_test)
# Get the models predicted price values 
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
print(predictions.shape)    
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
fig = px.line(x=train_df["Date"], y=train_df["Train"],title='Stock Price Prediction')
fig.add_scatter(x=valid_df["Date"], y=valid_df["Val"], mode='lines', name='Val', line=dict(color='orange'))
fig.add_scatter(x=valid_df["Date"], y=valid_df["Predictions"], mode='lines', name='Predictions', line=dict(color='red'))
fig.update_traces(line={'width': 2})
# Customize the plot
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Close Price INR',
    font=dict(size=18),
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01)
)
fig.show()
#---------------------------------------------------------------------------------------
# today = datetime.today().date()
# last_60_days = dataset[60:]
# # Scale the last 60 days data
# scaler = MinMaxScaler(feature_range=(0, 1))
# last_60_days_scaled = scaler.fit_transform(last_60_days.reshape(-1, 1))
# # Prepare the data for prediction
# x_test = []
# for i in range(60, len(test_data)):
#     x_test.append(last_60_days_scaled[i - 60:i, 0])
# print(len(x_test))
# # Convert the data to a numpy array
# x_test = np.array(x_test)
# # Reshape the data
# x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
# # print(x_test.shape)
# # Load the pre-trained model
# model = keras.models.load_model("StockMarketPredictor.h5")
# # Get the predictions
# predictions = model.predict(x_test)
# # Undo the scaling to get the actual values
# predictions = scaler.inverse_transform(predictions)
# Print the predictions for the next 60 days
# start_date = today
# for i in range(len(predictions)):
#     prediction_date = start_date + timedelta(days=i)
#     print(f"{prediction_date}: {predictions[i][0]}")
last_60_days = dataset[-60:]
# print(last_60_days)
# Create an empty list to store the next 60 days' data
# next_60_days = []
# Append the last 60 days to the list
next_60_days = last_60_days[:60]
# print(next_60_days)
# Scale the data
next_60_days = scaler.transform(next_60_days)
# Create a new dataset for the next 60 days
future_data = []
# Iterate over the next 60 days and create a dataset
for i in range(60, 120):
    future_data.append(next_60_days[i-60:i])

print(future_data)
# Convert the future_data to a numpy array
future_data = np.array(future_data)
print(future_data.shape)
# Reshape the data to match the input shape of the model
future_data = np.reshape(future_data, (future_data.shape[0], future_data.shape[1], -1))
# Use the model to make predictions on the future data
future_predictions = model.predict(future_data)
# Inverse transform the predictions to get the actual stock prices
future_predictions = scaler.inverse_transform(future_predictions)
