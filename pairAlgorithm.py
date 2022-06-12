import datetime as dt
import searchStock as ss
from matplotlib import dates
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests
import statsmodels.tsa.stattools as ts

def plot_chart(value, dates):
    
    floatsArr = [eval(x) for x in value]
    
    value = np.array(floatsArr)
    dates = np.array(dates)

    #x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]
    
    for val in dates:
        print(val)
    
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    
    #plt.plot(dates, value)
    #plt.show()
    #plt.gcf().autofmt_xdate()

def cointegrated_pairs(symbol):
    year_value, year_dates = get_last_year(symbol)
    plot_chart(year_value, year_dates)
    
def get_last_year(symbol):
    value, Dates = ss.values_dates(symbol)
    year_dates = Dates[-252:]
    year_value = value[-252:]
    return year_value, year_dates
    
if __name__ == '__main__':
    cointegrated_pairs('AAPL')
    #plot_chart()