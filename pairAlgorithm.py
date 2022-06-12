from cProfile import label
import datetime as dt
import searchStock as ss
from matplotlib import dates
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests
import statsmodels.tsa.stattools as ts

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

def cointegrated_pairs(symbols):
    print('pairs')
    
def run_graph(symbols):
    values = []
    dates = []
    for val in symbols:
        year_value, year_dates = get_last_year(val)
        values.append(year_value)
        dates.append(year_dates)
    plot_chart(values, dates, symbols)
    
def get_last_year(symbol):
    value, Dates = ss.values_dates(symbol)
    year_dates = Dates[-252:]
    year_value = value[-252:]
    return year_value, year_dates
    
if __name__ == '__main__':
    vals = ['AAPL', 'AAL', 'ADS']
    #cointegrated_pairs(vals)
    #plot_chart()
    run_graph(vals)