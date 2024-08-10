import requests
import pandas as pd
import json
import csv
import matplotlib.pyplot as plt
import upstox_client
from upstox_client.rest import ApiException

api_version = "2.0"

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
to_date = '2023-11-13'
from_date = '2023-11-12'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)


# CSV = pd.DataFrame(data)
# CSV.to_csv("out.csv", index=False)

# print(json_data)

# df = pd.read_csv("ohlc_data.csv")
# df.set_index("Timestamp", inplace=True)
# print(df.head())

# plt.plot(df["Close"])
# plt.show()
# import csv

# nse_isin_dict = {}
# temp_dict = {}
# with open('Eligible_Securities.csv', 'r') as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip the header row
#     for row in reader:
#         # print(row[0], row[1], row[4])
#         temp_str = str(row[0])
#         temp_dict["isin"] = temp_str
#         temp_str = str(row[1])
#         temp_dict["name"] = temp_str
#         nse_isin_dict[row[4]] = temp_dict
# print(nse_isin_dict)