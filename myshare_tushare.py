import pandas as pd
import tushare as ts
import myshare_util as msu
from console_progressbar import ProgressBar

def get_full_data(pro, code, year, now):
    num = 100000000
    df_basic = pro.query('daily_basic', ts_code=code, trade_date=now)
    df_income = pro.income(ts_code=code, period=year)
    df_fina = pro.fina_indicator(ts_code=code, period=year)
    # DataFrame pd
    df_new = df_income.merge(df_basic, on='ts_code', how='outer')
    df_dat = df_new.merge(df_fina, on='ts_code', how='outer')
    total_mv = df_dat.at[0, 'total_mv'] / 10000
    df_dat.at[0, 'total_mv'] = total_mv
    total_revenue = df_dat.at[0, 'total_revenue'] / num
    df_dat.at[0, 'total_revenue'] = total_revenue
    total_profit = df_dat.at[0, 'total_profit'] / num
    df_dat.at[0, 'total_profit'] = total_profit
    return df_dat

def get_data(pro, code, year, now):
    df_dat = get_full_data(pro, code, year, now)
    return df_dat[['ts_code','close','pe_ttm','bps','total_mv','total_revenue',
        'total_profit','basic_eps','profit_to_gr','op_yoy']]

def save_to_csv(pro, now = '20190605', year = '20181231', index_file='data/sse_ms20.txt'):
    """ 
    Save data to a file in csv format. The index file can be sse50.txt, myshare.txt
    or sse_dividend.txt.
    """
    print(index_file)
    sse50 = [x.rstrip()+'.SH' for x in open(index_file)]
    i=0
    pb = ProgressBar(total=100,prefix='Downloading', suffix='', decimals=3, length=50, fill='*', zfill='-')
    num = len(sse50)
    for code in sse50:
        if i == 0:
            data = get_data(pro, code, year, now)
            data.columns=['代码', '最新价', '市盈率', '市净率', '总市值(亿元)', '主营业务收入(亿元)', '净利润(亿元)', '每股收益', '利润率', '利润增长率(%)']
            i = i + 1
            pb.print_progress_bar((i/num)*100)
        else:
            new = get_data(pro, code, year, now)
            new.columns=['代码', '最新价', '市盈率', '市净率', '总市值(亿元)', '主营业务收入(亿元)', '净利润(亿元)', '每股收益', '利润率', '利润增长率(%)']
            data.loc[i] = new.loc[0]
            i = i + 1
            pb.print_progress_bar((i/num)*100)
            # print(new)

    data_file_name = 'build/' + msu.file_base_name(index_file) + '.csv'
    print('Saving to '+data_file_name)
    data.to_csv(data_file_name)
    return data

def get_full_dividend(pro, code):
    return pro.dividend(ts_code=code)

# print (data)