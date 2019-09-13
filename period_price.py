from datetime import date, timedelta
from urllib.request import urlopen
from dateutil import rrule
import os
import datetime
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Get period price of single stock
# Then output as chart

def craw_one_month(stock_num, date):
    url = ("http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+
        "&stockNo="+
        str(stock_num))

    data = json.loads(urlopen(url).read())
    return pd.DataFrame(data['data'], columns=data['fields'])

def craw_stock(stock_num, start_month):
    begin_month = date(*[int(x) for x in start_month.split('-')])
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    end_month = date(*[int(x) for x in now.split('-')])

    result = pd.DataFrame()

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=begin_month, until=end_month):
        result = pd.concat([result, craw_one_month(stock_num, dt)], ignore_index=True)
        # Delay a moment to avoid block by server
        time.sleep(2000.0/1000.0)

    return result
    
def draw_chart(df):
    df['收盤價'] = df['收盤價'].astype(float)
    df.loc[:]['收盤價'].plot(figsize=(9, 4))
    plt.xlabel('month')
    plt.ylabel('stock')
    plt.show()

def save_as_csv(filename, df):
    folder_name = 'period_price'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    df.to_csv(os.path.join(folder_name, filename), encoding='utf_8_sig')
     

# Get TSMC as example, from 2019/1/1 to Today
df = craw_stock(2330, '2019-9-1')
print(df)
df.set_index('日期', inplace=True)
print(df)

# Drop some information
df = df.drop(['成交金額'], axis=1)
df = df.drop(['成交股數'], axis=1)
print(df)

# Plot the price chart
draw_chart(df)

#Save as .csv file
save_as_csv('tsmc.csv', df)