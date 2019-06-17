import pandas as pd
# from pandas_datareader import data as pdr
import yfinance as yf
import myshare_util as msu
from console_progressbar import ProgressBar

# yf.pdr_override() 

# download dataframe
# data = pdr.get_data_yahoo("GOOG", start="2019-05-27", end="2019-05-31")

def save_to_csv(data, index_file):
    data_file_name = 'build/' + msu.file_base_name(index_file) + '_yf.csv'
    print('Saving to '+data_file_name)
    data.to_csv(data_file_name)

def save_full_data(stock_index, index_file):
    print(stock_index)
    i=0
    pb = ProgressBar(total=100,prefix='Downloading', suffix='', decimals=3, length=50, fill='*', zfill='-')
    num = len(stock_index)
    ydata = {}
    for stock in stock_index:
        ticker = yf.Ticker(stock)
        ydata[ticker.info['symbol']] = ticker.info
        i = i + 1
        pb.print_progress_bar((i/num)*100)

    ydata_frame = pd.DataFrame(ydata).T
    save_to_csv(ydata_frame, index_file)
    return ydata_frame

def get_yf_data(stock_index, index_file):
    print(stock_index)
    i=0
    pb = ProgressBar(total=100,prefix='Downloading', suffix='', decimals=3, length=50, fill='*', zfill='-')
    num = len(stock_index)
    ydata = {}
    for stock in stock_index:
        ticker = yf.Ticker(stock)
        ydata[ticker.info['symbol']] = ticker.info
        i = i + 1
        pb.print_progress_bar((i/num)*100)

    ydata_frame = pd.DataFrame(ydata).T[['longName', 'regularMarketPreviousClose', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow','forwardPE','marketCap']]
    ydata_frame.columns=['名称','最新价','52周最高','52周最低','市盈率','总市值']
    ydata_frame['总市值']=ydata_frame['总市值']/100000000
    return ydata_frame

def save_data(stock_index, index_file):
    ydf = get_yf_data(stock_index, index_file)
    save_to_csv(ydf, index_file)
    return ydf

def save_sse_data(sse_index_file='data/sse_ms20.txt'):
    print(sse_index_file)
    sse_stock_index = [x.rstrip()+'.SS' for x in open(sse_index_file)]
    return save_data(sse_stock_index, sse_index_file)

def save_hk_data(hk_index_file='data/hk_ms20.txt'):
    print(hk_index_file)
    hk_stock_index = [x.rstrip()+'.HK' for x in open(hk_index_file)]
    return save_data(hk_stock_index, hk_index_file)

def save_ses_data(ses_index_file='data/ses_ms20.txt'):
    print(ses_index_file)
    ses_stock_index = [x.rstrip()+'.SI' for x in open(ses_index_file)]
    return save_data(ses_stock_index, ses_index_file)

def save_us_data(us_index_file='data/us_ms20.txt'):
    print(us_index_file)
    us_stock_index = [x.rstrip() for x in open(us_index_file)]
    return save_data(us_stock_index, us_index_file)


