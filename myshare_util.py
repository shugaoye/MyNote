import os
import pandas as pd
import tushare as ts
from datetime import datetime

def to_date(sdate):
    d1=sdate[0:4]+'-'+sdate[4:6]+'-'+sdate[6:8]
    return datetime.strptime(d1, '%Y-%m-%d')

def file_base_name(file_name):
    filename = os.path.basename(file_name)
    if '.' in filename:
        separator_index = filename.index('.')
        base_name = filename[:separator_index]
        return os.path.basename(base_name)
    else:
        return os.path.basename(filename)

def init_tushare_api():
    f = open('build/token.txt')
    token = f.readline()
    ts.set_token(token)
    return ts.pro_api()

def save_to_csv(data, index_file):
    data_file_name = 'build/' + file_base_name(index_file) + '_div.csv'
    print('Saving csv file to '+data_file_name)
    data.to_csv(data_file_name)

def save_to_excel(data, index_file, sheet='cn'):
    data_file_name = 'build/' + file_base_name(index_file) + '_holding.xlsx'
    print('Saving excel file to '+data_file_name)
    writer = pd.ExcelWriter(data_file_name)
    data.to_excel(writer, sheet)
    writer.save()