import os
import requests
import pandas as pd
import numpy as np
from io import StringIO

# Get all stock price of day
# And save as csv


def get_data(date):
    if (len(date) != 8) or (int(date) < 0):
        print('Date format error\nexample: 20190915')
        return

    resp = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='
    + date + '&type=ALL')

    index_lst = []
    ETF_lst = []
    stock_lst = []

    for i in resp.text.split('\n'):
        # Respond json format: 1.index indexes 2.ETF 3.stock
        # Examples:
        #   index : "臺灣50指數","8,146.44","+","37.34","0.46",
        #   ETF   : ="0050","元大台灣50","12,633,348","4,942","1,058,619,857","83.70","84.00","83.65","83.80","+","0.30","83.75","6","83.80","9","0.00",
        #   stock : "2330","台積電","17,317,833","8,762","4,585,545,966","265.50","266.00","263.50","265.00","+","1.50","264.50","49","265.00","344","21.67",
        data_len = len(i.split('",'))
        if data_len == 6:
            index_lst.append(i)
        else:
            if i.startswith('='):
                ETF_lst.append(i.split('=')[1])
            elif data_len == 17:
                stock_lst.append(i)

    # save as csv
    folder_name = os.path.join('day_all_price', date) 

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # indexes
    filename = 'index.csv'
    df = pd.read_csv(StringIO('\n'.join(index_lst)), error_bad_lines=False)
    df.columns = ["指數","收盤指數","漲跌(+/-)","漲跌點數","漲跌百分比(%)",""]
    df.to_csv(os.path.join(folder_name, filename), encoding='utf_8_sig')

    # ETF
    filename = 'ETF.csv'
    df = pd.read_csv(StringIO('\n'.join(ETF_lst)), error_bad_lines=False)
    df.columns = ["證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價",
    "收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",""]
    df.to_csv(os.path.join(folder_name, filename), encoding='utf_8_sig')

    # stocks
    filename = 'stock.csv'
    df = pd.read_csv(StringIO('\n'.join(stock_lst)), error_bad_lines=False)
    df.columns = ["證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價",
    "收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",""]
    df.to_csv(os.path.join(folder_name, filename), encoding='utf_8_sig')

get_data('20190909')
get_data('20190910')