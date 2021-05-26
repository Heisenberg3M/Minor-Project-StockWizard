from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post
from .forms import TickerForm
from datetime import datetime

import yfinance as yf
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from newsapi import NewsApiClient
#from django.http import HttpResponse

# Create your views here.

stock_symbol_name=""
stock_news=None

def home(request):
    global stock_symbol_name
    stock_symbol_name=""
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm()

    return render(request, 'stocks/home.html', {'form': form})

def ticker(request, tid):
    try:
        stock=yf.Ticker(tid)
        s=stock.info
        summary = {}
        summary['ticker'] = tid.upper()
        summary['symbol']=s['symbol']
        summary['description']=s['longBusinessSummary']
        summary['name']=s['longName']
        summary['open']=s['open']
        summary['high']=s['regularMarketDayHigh']
        summary['low']=s['dayLow']
        summary['close']=s['previousClose']
        summary['volume']=s['volume']
        summary['adjOpen']=s['open']
        summary['adjHigh']=s['regularMarketDayHigh']
        summary['adjLow']=s['dayLow']
        summary['adjClose']=s['previousClose']
        summary['adjVolume']=s['volume']
        summary['show'] = True
        
        global stock_symbol_name
        stock_symbol_name=tid.upper()
        
        # news
        global stock_news
        newsapi=NewsApiClient(api_key='c487a57cd85444eab7fc473262abf83e')
        all_articles = newsapi.get_everything(q=stock_symbol_name,from_param='2021-05-01',language='en')
        stock_news=all_articles['articles']
        summary["news"] = stock_news
        '''
        for i in l:
            print(i['author'])
            print(i['title'])
            print(i['description'])
            print(i['publishedAt'])
            print('\n')
        '''
        return render(request, 'stocks/home.html', summary)
    except:
        err={}
        err['error']="Invalid Stock symbol."
        err['hasError']=True
        return render(request, 'stocks/home.html', err)
    

def about(request):
    about={}
    about['search']=True
    return render(request, 'stocks/about.html', about)

def watchlist(request):
    watchlist={}
    watchlist["search"]=True
    return render(request, 'stocks/watchlist.html', watchlist)


def historical(request):
    if stock_symbol_name=="":
        err={}
        err['error']="Search stock first"
        err['hasError']=True
        err['search']=True
        return render(request, 'stocks/historical_data.html', err)
    else:
        stock=yf.Ticker(stock_symbol_name)
        start_date='2021-01-01'
        historical_data=stock.history(start=start_date)
        historical_data = historical_data.reset_index()
        for i in ['Open', 'High', 'Close', 'Low']: 
            historical_data[i]  =  historical_data[i].astype('float64')
        # Getting date from DataFrame
        date_data=historical_data['Date']
        date_data=date_data.tolist()
        date_data_list=[]
        for date in date_data:
            d=date.to_pydatetime().strftime("%d-%m-%Y")
            date_data_list.append(d)
        # Getting High details for ticker
        high_data=historical_data['High']
        high_data=high_data.tolist()
        historical={}
        historical['date']=date_data_list
        historical['high']=high_data
        historical['show']=True
        historical["news"]=stock_news
        historical["ticker"]=stock_symbol_name
        historical['search']=True

        return render(request, 'stocks/historical_data.html', historical)

def prediction(request):
    if stock_symbol_name=="":
        err={}
        err['error']="Search stock first"
        err['hasError']=True
        err['search']=True
        return render(request, 'stocks/prediction.html', err)
    else:
        # training models
        stock=yf.Ticker(stock_symbol_name)
        start_date='2010-11-01'
        historical_data=stock.history(start=start_date)
        historical_data=historical_data.reset_index()
        historical_data=historical_data.iloc[:,1:2]
        training_data=historical_data
        mm = MinMaxScaler(feature_range = (0, 1))
        training_data = mm.fit_transform(training_data)
        x_train = training_data[0:1257]
        y_train = training_data[1:1258]
        x_train = np.reshape(x_train, (1257, 1, 1))
        model = Sequential()
        model.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, 1)))
        model.add(Dense(units = 1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        model.fit(x_train, y_train, batch_size = 32, epochs = 100)

        # predicting data
        historical_data=stock.history(start=start_date)
        historical_data=historical_data.reset_index()
        historical_data=historical_data.iloc[:,1:2]
        mm=MinMaxScaler(feature_range = (0, 1))
        inputs=mm.fit_transform(historical_data)
        inputs=np.reshape(inputs, (len(historical_data), 1, 1))
        predicted_stock_price = model.predict(inputs)
        predicted_stock_price = mm.inverse_transform(predicted_stock_price)
        predicted_price=[]
        count=0
        for p in predicted_stock_price:
            predicted_price.append(p[0])
            count+=1
            if count>50: break
        prediction_data={}
        prediction_data["price"]=predicted_price
        prediction_data["show"]=True
        prediction_data["ticker"]=stock_symbol_name
        prediction_data["news"]=stock_news
        prediction_data['search']=True

        return render(request, 'stocks/prediction.html', prediction_data)

