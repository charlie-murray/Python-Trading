# All the imports I need for my system to run
from ctypes import resize
import datetime as dt
from itertools import combinations
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

# Function used to plot regualar list of data
def plot_chart(value, dates, symbols):
    
    for i in range(0, len(value)):
        
        floatsArr = [eval(x) for x in value[i]] # sets the stock prices from str to float
        
        value[i] = np.array(floatsArr) # Creates numpy array of prices
        dates[i] = np.array(dates[i]) # Creates numpy array of dates

        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates[i]] # Sets the dates format
        
        plt.plot(x, value[i], label="" + symbols[i] + "") # Sets the name of each line
    
    # Plots the data
    plt.xlabel('Stock Dates')
    plt.ylabel('Stock Prices')
    plt.legend()
    plt.show()

# Function used to get the last year of data, connected through interface
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

# Gets the last year of data from S&P data csv
def get_last_year(symbol):
    value, Dates = ss.values_dates(symbol)
    year_dates = Dates[-252:] # Picks out all dates from the last year
    year_value = value[-252:] # Picks out all the prices from the last year
    return year_value, year_dates

# Function get all stock prices from time which is set
# Used in more accurate analysis
def get_prices(stocks):
    start = '2020-12-31'
    end = '2022-03-08'
    
    data = pd.DataFrame()
    
    for stock in stocks:
        prices = yf.download(stock, start, end) # Gets stock prices from yahoo
        data[stock] = prices['Close']
        
    return data

# Works out the cointergration of all the stock combinations
def cointegrated_calculator(file):
    
    all_stocks = []
    
    # Reads all stocks that need to be searched
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader: all_stocks.append(row)

    # Gets the price of all the stocks
    data = get_prices(all_stocks)
    
    p_values = pd.DataFrame()
    
    for i in data:
        p_col = []
        for j in data:
            if i != j:
                result = adfuller(data[i] - data[j])
                p_col.append(result[1])
            else: p_col.append(0.0)
        p_values[i] = p_col
    
    p_values.to_csv('p_value.csv', index = False, header=True) # Prints all the cointergration numbers to csv

# Calculates the trading singals for the algorithm
def calculate_signals(stocks):
    
    strSplit = stocks.split(',')
    stock = [strSplit[0], strSplit[1]]
    
    stock_frame = get_prices(stock)
    
    # Adds the two stocks and their range to a dataframe
    stock_frame = stock_frame.join(pd.concat([stock_frame[a].div(stock_frame[b]).
                        rename(f'{a}/{b}') for a, b in combinations(stock_frame.columns, 2)], 1))
    
    plt.plot(stock_frame.index, stock_frame['CDNS/VRSK'])
    plt.show()

# Calculates how cointergrated the stocks are
def calculate_pairs(file):
    
    p_values = pd.read_csv(file)
    
    tradeable = []
    
    for stock in p_values:
        stock_pval = p_values[stock]
        for p in stock_pval:
            if p != 0.0 and p < 0.05: # if they are cointergrated then added to tradable
                stock_row = p_values[p_values[stock] == p].index[0]
                y_stock = p_values.columns[stock_row]
                test_stock = y_stock + "," + stock
                if test_stock not in tradeable: tradeable.append(stock + "," + y_stock + "," + str(p))
    
    best_pair(tradeable)

# Works out the most cointergrated pair of stocks
def best_pair(stocks):
    
    best_stock = 'x,y,0.05'
    
    for stock in stocks:
        option1 = stock.split(',')
        option2 = best_stock.split(',')
        if float(option1[2]) < float(option2[2]): best_stock = stock
    
    calculate_signals(best_stock) # Works out signals for the best pair

if __name__ == '__main__':
    #cointegrated_calculator('list_of_stocks.csv')
    #plot_chart()
    #run_graph(vals, 'y')
    calculate_pairs('p_value.csv')