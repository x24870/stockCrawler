import requests
import pandas as pd
import numpy as np
from io import StringIO

date = '20190909'
resp = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='
+ date + '&type=ALL')

index_lst = []
ETF_lst = []
stock_lst = []
a = 0
for i in resp.text.split('\n'):
    # Respond json format: 1.stock indexes 2.ETF 3.stock
    if len(i) < 17: # stock indexes
        index_lst.append(i)
    elif i.startswith('='): #ETF
        ETF_lst.append(i)
    else: #stock
        stock_lst.append(i)
    a += 1

print(a)
print(len(index_lst))
print(len(ETF_lst))
print(len(stock_lst))
