from ctypes import resize
import datetime as dt
from unittest import result
import searchStock as ss
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import yfinance as yf
import scipy.optimize as spop
import pandas_datareader as web
import csv
from statsmodels.tsa.stattools import adfuller

def plot_chart(value, dates, symbols):
    
    for i in range(0, len(value)):
        
        floatsArr = [eval(x) for x in value[i]]
        
        value[i] = np.array(floatsArr)
        dates[i] = np.array(dates[i])

        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates[i]]
        
        plt.plot(x, value[i], label="" + symbols[i] + "")
    
    plt.xlabel('Stock Dates')
    plt.ylabel('Stock Prices')
    plt.legend()
    plt.show()
    
def run_graph(symbols, last_year):
    values = []
    dates = []
    for val in symbols:
        if last_year == 'y':
            year_value, year_dates = get_last_year(val)
            values.append(year_value)
            dates.append(year_dates)
        else:
            Value, Dates = ss.values_dates(val)
            values.append(Value)
            dates.append(Dates)
            
    plot_chart(values, dates, symbols)
    
def get_last_year(symbol):
    value, Dates = ss.values_dates(symbol)
    year_dates = Dates[-252:]
    year_value = value[-252:]
    return year_value, year_dates

def cointegrated_calculator(file):
    start = '2020-12-31'
    end = '2022-03-08'
    
    all_stocks = []
    
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        for row in spamreader:
            if i != 0:
                strSplit = row[0].split(',')
                all_stocks.append(strSplit[0])
            i += 1 
    
    data = pd.DataFrame()
    
    for stock in all_stocks:
        prices = yf.download(stock, start, end)
        data[stock] = prices['Close']
    
    p_values = pd.DataFrame()
    
    for i in data:
        p_col = []
        for j in data:
            if i != j:
                result = adfuller(data[i] - data[j])
                p_col.append(result[1])
            else:
                p_col.append(0.0)
        p_values[i] = p_col
    
    p_values.to_csv('p_value.csv', index = False, header=True)

def calculate_signals(stocks):
    
    start = '2020-12-31'
    end = '2022-03-08'
    
    strSplit = stocks.split(',')
    stock = [strSplit[0], strSplit[1]]
    p_value = strSplit[2]
    
    stock_frame = pd.DataFrame()
    
    for s in stock:
        prices = yf.download(s, start, end)
        stock_frame[s] = prices['Close']
        
    ratio_stock = pd.DataFrame()

    for i in range(0, len(stock_frame.index)):
        stock_values = []
        for symbol in stock_frame:
            stock_values.append(stock_frame.loc[i][symbol])
        ratio_stock.append({'ratios':stock_values[0]/stock_values[1]})
    
    plt.plot(ratio_stock)
    plt.show()

    
def calculate_pairs(file):
    
    p_values = pd.read_csv(file)
    
    tradeable = []
    
    for stock in p_values:
        stock_pval = p_values[stock]
        for p in stock_pval:
            if p != 0.0 and p < 0.05:
                stock_row = p_values[p_values[stock] == p].index[0]
                y_stock = p_values.columns[stock_row]
                test_stock = y_stock + "," + stock
                if test_stock not in tradeable:
                    tradeable.append(stock + "," + y_stock + "," + str(p))
    
    best_pair(tradeable)

def best_pair(stocks):
    
    best_stock = 'x,y,0.05'
    
    for stock in stocks:
        option1 = stock.split(',')
        option2 = best_stock.split(',')
        if float(option1[2]) < float(option2[2]):
            best_stock = stock
    
    calculate_signals(best_stock)

if __name__ == '__main__':
    #cointegrated_calculator('list_of_stocks.csv')
    #plot_chart()
    #run_graph(vals, 'y')
    calculate_pairs('p_value.csv')