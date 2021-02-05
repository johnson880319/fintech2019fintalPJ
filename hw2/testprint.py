import talib
import pandas as pd

df=pd.read_csv("SPY.csv")
df['MACD'], df['MACDsignal'], df['MACDhist'] = talib.MACD(df['Adj Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
print(df)