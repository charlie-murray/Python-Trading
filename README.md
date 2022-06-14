# Python-Trading

This is a python programing project over the summer of 2022

ALSO SAVING PARTIAL BITS OF DATA IN HERE I MIGHT NEED LATER

start = '2020-12-31'
    end = '2022-03-08'
    fee = 0.001
    window = 252
    t_threshold = -2.5
    
    #start = dt(2017, 1, 1)
    symbols_list = ['AAPL', 'F', 'TWTR', 'FB', 'AAL', 'AMZN', 'GOOGL', 'GE']
    
    symbols=[]

    #pull price using iex for each symbol in list defined above
    for ticker in symbols_list: 
        r = yf.download(ticker, start, end)
        # add a symbol column
        r['Symbol'] = ticker 
        symbols.append(r)

    # concatenate into df
    df = pd.concat(symbols)
    df = df.reset_index()
    df = df[['Date', 'Close', 'Symbol']]
    
    #have to pivot the df
    df_pivot = df.pivot('Date','Symbol','Close').reset_index()
    df_pivot.head()
    
    corr_df = df_pivot.corr(method='pearson')
    #reset symbol as index (rather than 0-X)
    corr_df.head().reset_index()
    
    print(corr_df)