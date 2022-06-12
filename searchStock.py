from optparse import Values
from symtable import Symbol
from matplotlib import dates
import pairAlgorithm as pa
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import math
import csv
from csv import writer

def values_dates(symbol):
    
    Values = []
    Dates = []
            
    with open('Historical_Data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        throughRow = 0
        for row in spamreader:
            strSplit = row[0].split(',')
            if throughRow == 0:
                for val in strSplit:
                    Dates.append(val)
                Dates.pop(0)
                throughRow +=1
            if strSplit[0] == symbol:
                for i in range(0, len(strSplit)):
                    if i != 0:
                        Values.append(strSplit[i])
                        throughRow += 1
        
    return Values, Dates

def dateSearch(symbol):
    try:
        while True:
            ans = input('\nEnter A Date [YEAR-MN-DY]: ')
            
            Values, Dates = values_dates(symbol)
            
            for i in range(0, len(Dates)):
                if Dates[i] == ans:
                    print('\nDate: ' + Dates[i])
                    print('\nPrice: ' + Values[i])
            
            runAgain = input("\nAnother Date? y/n: ")
            
            if runAgain == 'n':
                break
    
    except Exception as e:
        print(e)
        
        
def searchStock(symbol):

    try:
        API_KEY = 'pk_c9d202a04afd4f45a1ffa4ec75e44e56'

        api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={API_KEY}'
        data = requests.get(api_url).json()
        
        print("Company Name: " + str(data['companyName']) + "\nLatest Price: " + str(data['latestPrice']) + "\nMarket Cap: " + 
            str(data['marketCap']) + "\nPercentage Change: " + str(data['changePercent']) + "\n52 Week High: " + str(data['week52High']) + 
            "\n52 Week Low: " + str(data['week52Low']) + "\nVolume: " + str(data['volume']) + "\nOpen: " + str(data['open']) + "\nClose: " + str(data['close']))
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    # sortData.py executed as script
    searchStock()
    dateSearch()