import os
import pandas as pd
import requests
import numpy as np
from io import StringIO

# Get target web site
date = '107_5'
url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+ date +'_0.html'
# This page contains many <table> tag
# It's suitable to use read_html() to get table
a = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})

#Use big5 enconding to avoid garbled
a.encoding = 'big5'
html_df = pd.read_html(a.text, header=0)

#Discard invalid table
df = pd.DataFrame()
folder_name = 'month_all_price'
filename = 'month_price.csv'
if not os.path.exists(folder_name): os.mkdir(folder_name)

whole_df = pd.DataFrame()
for idx, df in enumerate(html_df):
    if df.shape[1] == 11:
        df.to_csv(os.path.join(folder_name, filename+str(idx)), encoding='utf_8_sig')
        whole_df = pd.concat([whole_df, df], ignore_index=True)

# Set column name
whole_df.columns = ['公司代號','公司名稱','當月營收','上月營收','去年當月營收','上月比較增減(%)','去年同月增減(%)',
'當月累計營收','去年累計營收','前期比較增減(%)','備註']

# Drop unneeded row
whole_df = whole_df[whole_df['公司代號'] != '合計']
whole_df = whole_df[whole_df['公司代號'] != '公司代號']

# Resort the sequance by index
whole_df = whole_df.set_index('公司代號')
whole_df = whole_df.sort_index()
#whole_df = whole_df.reset_index(drop=True)

# Save as .csv
whole_df.to_csv(os.path.join(folder_name, filename), encoding='utf_8_sig')






# # 3.4 重新排序索引值
# #df = df.reset_index(drop=True) 