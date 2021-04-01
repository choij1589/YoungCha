import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from AnalysisTools.CandlestickMaker import CandlestickMaker

df = pd.read_csv("./data/coin_Bitcoin.csv")
df = df[['Date', 'High', 'Low', 'Open', 'Close', 'Volume']]

# preprocess
for idx in df.index:
    if df.loc[idx, 'Volume'] == 0.:
        df.loc[idx, 'Volume'] = np.nan
    date_time = df.loc[idx, 'Date'].split(" ")
    date, time = date_time[0], date_time[1]
    df.loc[idx, 'Date'] = datetime.strptime(date, '%Y-%m-%d').date()
df = df.set_index('Date')
df = df.dropna()

# set daily returns and accumulated returns
#df['rtn'] = df['Close'].pct_change()
#df['acc_rtn'] = (1.0 + df['rtn']).cumprod()

# train dataset
TrainMaker = CandlestickMaker(df, "2015-01-01", "2019-12-31")
TrainMaker.ohlc_to_candlestick(days=5, coin_name="coin_Bitcoin", train=True, use_volume=False)

# test dataset
TestMaker = CandlestickMaker(df, "2020-01-01", "2020-12-31")
TestMaker.ohlc_to_candlestick(days=5, coin_name="coin_Bitcoin", train=False, use_volume=False)
