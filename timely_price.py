from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import requests
import sched
import time
import json

s = sched.scheduler(time.time, time.sleep)

def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color

def stock_crawler(targets):
    
    clear_output(wait=True)
    
    # compose query url
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets)
    
    #　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    data = json.loads(urlopen(query_url).read())

    # filter needed columns
    columns = ['c','n','z','tv','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號','公司簡稱','當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價','昨收價']
    df.to_csv('timely_price.csv')
    
    # adding up-down percentage
    df.iloc[:, [2,3,4,5,6,7,8]] = df.iloc[:, [2,3,4,5,6,7,8]].astype(float)
    df['漲跌百分比'] = (df['當盤成交價'] - df['昨收價'])/df['昨收價'] * 100
    
    # record updating time
    time = datetime.datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute))
    
    # show table
    df = df.style.applymap(tableColor, subset=['漲跌百分比'])
    display(df)
    
    start_time = datetime.datetime.strptime(str(time.date())+'9:30', '%Y-%m-%d%H:%M')
    end_time =  datetime.datetime.strptime(str(time.date())+'13:30', '%Y-%m-%d%H:%M')
    
    # The condition to terminate crawler
    if time >= start_time and time <= end_time:
       s.enter(1, 0, stock_crawler, argument=(targets,))

stock_list = ['1101','1102','1103','2330']

s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()