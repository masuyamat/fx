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
    "count": 5000, # データ数を指定
        "granularity": "M10" # 1分間隔
}

# APIへ過去データをリクエスト
r = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
api.request(r)

# # APIから取得した最初のmid（中値）を確認
# print(r.response['candles'][1]['mid'])

# # 時間を確認
# print(r.response['candles'][0]['time'])

# dataとしてリストへ過去レートを変換
data = []
for raw in r.response['candles']:
    data.append([raw['time'], raw['volume'], raw['mid']['o'], raw['mid']['h'], raw['mid']['l'], raw['mid']['c']])

# リストをPandasのDataFrame形式へ変換
df = pd.DataFrame(data)
df.columns = ['Time', 'Volume', 'Open', 'High', 'Low', 'Close']
df = df.set_index('Time')
df.head() #無くても可

# date方がストリングで扱いづらいので、綺麗にする
df.index = pd.to_datetime(df.index)
df.tail() #無くても可

# DataFrameからCSVへ書き出し (easy)
df.to_csv('api-usdjpy-H1-0222.csv')
