
# coding: utf-8

# In[73]:


# API接続設定のファイルを読み込む
import configparser


# In[74]:


# ライブラリのインポート
import pandas as pd
import numpy as np
import seaborn
import datetime
import talib as ta
ta.get_function_groups


# In[75]:


# ローソク足描写
# 事前に " pip install https://github.com/matplotlib/mpl_finance/archive/master.zip"が必要


import matplotlib.pyplot as plt
import mpl_finance as mpf # 最近はこのモジュール
from mpl_finance import candlestick2_ohlc
from matplotlib import ticker
import matplotlib.dates as mdates
get_ipython().run_line_magic('matplotlib', 'inline')


# In[76]:


# データの読み込み
masta = pd.read_csv("api-usdjpy-M1-20190302.csv")
df = masta.copy()
chart = masta.copy()


# In[78]:


#不要な列を削除
del df['volume']
df.head()


# In[79]:


# データの日付をインデックスとして扱う
df.index = pd.to_datetime(df.time)


# In[80]:


# ローソク足チャート
def candlechart(data, width=0.8):
    fig, ax = plt.subplots()
 
    # ローソク足
    mpf.candlestick2_ohlc(ax, opens=data.open.values, closes=data.close.values,
                          lows=data.low.values, highs=data.high.values,
                          width=width, colorup='r', colordown='b')
 
    xdate = data.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
 
    def mydate(x, pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''
 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax.format_xdata = mdates.DateFormatter('%m-%d')
 
    fig.autofmt_xdate()
    fig.tight_layout()
 
    return fig, ax


# In[81]:


# カラム名を短く変更
# df.columns = ['t', 'o', 'h', 'l', 'c'] #一旦削除


# In[82]:


# OHLCデータをNumpy配列へ変換
o = np.array(df['open'])
c = np.array(df['close'])
l = np.array(df['low'])
h = np.array(df['high'])


# In[83]:


# 4種類のローソク足パターンを抽出
df['Marubozu'] = ta.CDLMARUBOZU(o, h, l, c)
df['Engulfing_Pattern'] = ta.CDLENGULFING(o, h, l, c)
df['Hammer'] = ta.CDLHAMMER(o, h, l, c)
df['Dragonfly_Doji'] = ta.CDLDRAGONFLYDOJI(o, h, l, c)


# In[84]:


# データの確認
df[10:15]


# In[85]:


#丸坊主のデータを確認
df[(df['Marubozu'] < 0) | (df['Marubozu'] > 0)].head()


# In[86]:


# 丸坊主のデータを確認
df['Marubozu'].loc['2019-01-14 10:20:00']


# In[91]:


# 丸坊主 陽線の位置を確認
set_time = datetime.datetime.strptime('2019-01-14 10:20:00', '%Y-%m-%d %H:%M:%S')
before = set_time - datetime.timedelta(hours=10)
after = set_time + datetime.timedelta(hours=10)
candlechart(df.loc[(df.index > before )&(df.index < after)])


# In[93]:


# 陽線 包み線が出る前後を表示
set_time = datetime.datetime.strptime('2019-01-14 06:30:00', '%Y-%m-%d %H:%M:%S')
before = set_time - datetime.timedelta(hours=10)
after = set_time + datetime.timedelta(hours=10)
candlechart(df.loc[(df.index > before )&(df.index < after)])


# In[95]:


# 陽線 カラカサ
set_time = datetime.datetime.strptime('2019-01-14 06:20:00', '%Y-%m-%d %H:%M:%S')
before = set_time - datetime.timedelta(hours=10)
after = set_time + datetime.timedelta(hours=10)
candlechart(df.loc[(df.index > before )&(df.index < after)])

