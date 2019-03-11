# coding: utf-8

# API接続設定のファイルを読み込む
import configparser

# レート取得のために必要なライブラリ
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

# 設定情報を"config_v1.txt"から読み込む
config = configparser.ConfigParser()
config.read('config_v1.txt') # パスの指定が必要です
account_id = config['oanda']['account_id']
api_key = config['oanda']['api_key']
api = API(access_token=api_key)

# 取得したい時間範囲を指定
params = {
    "count": 1000, # データ数を指定
        "granularity": "M1" # 1分間隔
}

# APIへ過去データをリクエスト
r = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
api.request(r)

# dataとしてリストへ過去レートを変換
data = []
for raw in r.response['candles']:
    data.append([raw['time'], raw['volume'], raw['mid']['o'], raw['mid']['h'], raw['mid']['l'], raw['mid']['c']])

# リストをPandasのDataFrame形式へ変換
df = pd.DataFrame(data)
df.columns = ['time', 'volume', 'open', 'high', 'low', 'close']
df = df.set_index('time')
df.head() #無くても可

# date方がストリングで扱いづらいので、綺麗にする
df.index = pd.to_datetime(df.index)
df.tail() #無くても可

# DataFrameからCSVへ書き出し (easy)
df.to_csv('api-usdjpy-M1.csv')


#########################################################################################
# ライブラリのインポート
import pandas as pd
import numpy as np
import seaborn
import datetime
import talib as ta
ta.get_function_groups

# ローソク足描写
import matplotlib.pyplot as plt
import mpl_finance as mpf # 最近はこのモジュール
from mpl_finance import candlestick2_ohlc
from matplotlib import ticker
import matplotlib.dates as mdates
# get_ipython().run_line_magic('matplotlib', 'inline')

# データの読み込み
masta = pd.read_csv("api-usdjpy-M1.csv")
df = masta.copy()
chart = masta.copy()

# データの日付をインデックスとして扱う
df.index = pd.to_datetime(df.time)

#不要な列を削除
del df['volume']
del df['time']

# # ローソク足チャート
# def candlechart(data, width=0.8):
#     fig, ax = plt.subplots()
#
#     # ローソク足
#     mpf.candlestick2_ohlc(ax, opens=data.open.values, closes=data.close.values,
#                           lows=data.low.values, highs=data.high.values,
#                           width=width, colorup='r', colordown='b')
#
#     xdate = data.index
#     ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
#
#     def mydate(x, pos):
#         try:
#             return xdate[int(x)]
#         except IndexError:
#             return ''
#
#     ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
#     ax.format_xdata = mdates.DateFormatter('%m-%d')
#
#     fig.autofmt_xdate()
#     fig.tight_layout()
#
#     return fig, ax

# OHLCデータをNumpy配列へ変換
o = np.array(df['open'])
c = np.array(df['close'])
l = np.array(df['low'])
h = np.array(df['high'])

# 4種類のローソク足パターンを抽出
df['Marubozu'] = ta.CDLMARUBOZU(o, h, l, c)

# 丸坊主のデータを確認
print(df[(df['Marubozu'] < 0) | (df['Marubozu'] > 0)].head())

# 丸坊主が出ている時の終値を抽出
time_marubozu = []
time_marubozu = df[df.Marubozu > 0]
# print(time_marubozu.head())
print(time_marubozu['close'].head())

# # 丸坊主のデータを確認
# df['Marubozu'].loc['2019-01-14 10:20:00']
