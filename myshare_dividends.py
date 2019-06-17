import pandas as pd
import tushare as ts
import myshare_tushare as mst
import myshare_util as msu
import yfinance as yf
from datetime import datetime
from console_progressbar import ProgressBar
from myshare_util import file_base_name

start_year = 2001
earliest_year = 2001

def set_earliest(year):
    global earliest_year
    if(year < earliest_year):
        earliest_year = year
    return earliest_year

def get_div_by_year(pro, code, channel):
    if channel == 'tushare':
        df_div = pro.dividend(ts_code=code)
        format = lambda x:datetime.strptime(x[0:4]+'-'+x[4:6]+'-'+x[6:8], '%Y-%m-%d')
        ds_div = pd.Series(list(df_div.cash_div),index=list(df_div['end_date'].map(format)))
    else:
        ds_div = yf.Ticker(code).dividends
    return ds_div.groupby([lambda x: x.year]).sum()

def get_div(pro, code, channel):
    global start_year
    ds_div = get_div_by_year(pro, code, channel)
    df_div = pd.DataFrame({code:ds_div}).T
    year = ds_div.index.min()
    if year > start_year:
        year = start_year
    else:
        year = set_earliest(year)
    while year < datetime.today().year:
        if year in ds_div:
            if year < start_year:
                df_div = df_div.drop(year, axis=1)
            year = year + 1
        else:
            df_div[year] = 0
            year = year + 1
    return df_div.sort_index(axis=1)
        
def get_dividend_data(pro, stock_index, index_file, channel):
    """ 
    Save data to a file in csv format.
    """
    i=0
    pb = ProgressBar(total=100,prefix='Downloading', suffix='', decimals=3, length=50, fill='*', zfill='-')
    num = len(stock_index)
    for code in stock_index:
        if i == 0:
            df_div = get_div(pro, code, channel)
            i = i + 1
            pb.print_progress_bar((i/num)*100)
        else:
            df_new = get_div(pro, code, channel)
            df_div.loc[code] = df_new.loc[code]
            i = i + 1
            pb.print_progress_bar((i/num)*100)
            # print(new)
    return df_div

def save_div(pro, index_file='data/sse_ms20.txt', start=2002, channel='t_sse'):
    """ 
    Save SSE data to a file in csv format. The index file can be sse50.txt, myshare.txt
    or sse_dividend.txt.
    channel can be:
    t_sse - tushare SSE
    y_sse - Yahoo SSE
    y_hk  - Yahoo Hong Kong
    y_ses - Yahoo Singapore
    y_US  - Yahoo US, this is the last case
    """
    global earliest_year
    if channel=='t_sse':
        stock_index = [x.rstrip()+'.SH' for x in open(index_file)]
    elif channel == 'y_sse':
        stock_index = [x.rstrip()+'.SS' for x in open(index_file)]
    elif channel == 'y_hk':
        stock_index = [x.rstrip()+'.HK' for x in open(index_file)]
    elif channel == 'y_ses':
        stock_index = [x.rstrip()+'.SI' for x in open(index_file)]
    else:
        stock_index = [x.rstrip() for x in open(index_file)]
    df_div = get_dividend_data(pro, stock_index, index_file, channel)
    year = earliest_year
    if start > earliest_year:
        while year < start:
            if year in df_div:
                df_div = df_div.drop(year, axis=1)
            year = year + 1
    msu.save_to_csv(df_div, index_file)
    return df_div
