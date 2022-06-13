import datetime as dt
import searchStock as ss
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import yfinance as yf
import scipy.optimize as spop

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

def cointegrated_pairs(stocks):
    start = '2019-12-31'
    end = '2021-03-08'
    fee = 0.001
    window = 252
    t_threshold = -2.5
    
    data = pd.DataFrame()
    returns = pd.DataFrame()
    
    for stock in stocks:
        prices = yf.download(stock, start, end)
        data[stock] = prices['Close']
        returns[stock] = np.append(data[stock][1:].reset_index(drop=True)/data[stock][:-1].reset_index(drop=True) - 1, 0)
    
    gross_returns = np.array([])
    net_returns = np.array([])
    t_s = np.array([])
    stock1 = stocks[0]
    stock2 = stocks[1]
    
    for t in range(window, len(data)):
        
        def unit_root(b):
            a = np.average(data[stock2][t-window:t] - b*data[stock1][t-window:t])
            fair_value = a + b*data[stock1][t-window:t]
            diff = np.array(fair_value - data[stock2][t-window:t])
            diff_diff = diff[1:] - diff[:-1]
            reg = sm.OLS(diff_diff, diff[:-1])
            res = reg.fit()
            return res.params[0]/res.bse[0]
        
        res1 = spop.minimize(unit_root, data[stock2][t]/data[stock1][t], method='Nelder-Mead')
        t_opt = res1.fun
        b_opt = float(res1.x)
        a_opt = np.average(data[stock2][t-window:t] - b_opt*data[stock1][t-window:t])
        fair_value = a_opt + b_opt*data[stock1][t]
        
        if t == window:
            old_signal = 0
        if t_opt > t_threshold:
            signal = 0
            gross_returns = 0
        else:
            signal = np.sign(fair_value - data[stock2][t])
            gross_returns = signal*returns[stock2][t] - signal*returns[stock1][t]
        
        fees = fee*abs(signal - old_signal)
        net_returns = gross_returns - fees
        gross_returns = np.append(gross_returns, gross_returns)
        net_returns = np.append(net_returns, net_returns)
        t_s = np.append(t_s, t_opt)
        
        print('day ' + str(data.index[t]))
        print('')
        if signal == 0:
            print('no trading')
        elif signal == 1:
            print('long position on ' + stock2 + ' and short position on ' + stock1)
        else:
            print('long position on ' + stock1 + ' and short position on ' + stock2)
        print('gross daily returns: ' + str(np.round(gross_returns*100, 2)) + '%')
        print('net daily returns: ' + str(np.round(net_returns*100, 2)) + '%')
        print('cumulative net returns so far: ' + str(np.round(np.prod(1+net_returns)*100-100, 2)) + '%')
        
        #plt.plot(np.append(np.cumprod(1+gross_returns)))
        #plt.plot(np.append(np.cumprod(1+net_returns)))
        
        plt.show()
        
if __name__ == '__main__':
    vals = ['AAPL', 'AAL']
    cointegrated_pairs(vals)
    #plot_chart()
    #run_graph(vals, 'y')