#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 15:01:55 2018

@author: rishisheth
"""

''' imports '''
import sqlalchemy
import pandas as pd
import pickle as pkl
import numpy as np

from fbprophet import Prophet
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings('ignore')

''' connect to rds on amazon '''
hostName = 'project-kojak1.cekiwi9udsce.us-east-2.rds.amazonaws.com'
user = 'Rishi'
pw = 'thisismypassword'
port = '5432'
database = 'dbsales'
this = 'postgres://' + user + ':' + pw + '@' + hostName + ':' + port + '/' + database

engine = sqlalchemy.create_engine(this)



''' gets dataframe involving specific store number and item number '''
def getDF(storeNum, itemNum):    
    myStore = pd.read_sql_query('SELECT * FROM "Sales" WHERE "store" = {} AND "item" = {}'.format(storeNum, itemNum), 
                                engine)
    myStore.date = pd.to_datetime(myStore.date)
    myStore = myStore.reset_index()
    myStore = myStore.drop(columns=['store', 'item', 'level_0', 'index'])
    myStore = myStore.sort_values('date')
    myStore.columns = ['ds', 'y']
    
    return myStore

''' calculate percent error to measure validity of model '''
def getPercentError(current, test):
    return (current-test)/current

''' test DF using ro to measure validity of model ''' 
def testDF(storeNum, itemNum, trainProportions=[0.5, 0.67, 0.75, 0.9]):
    storeItemDF = getDF(storeNum, itemNum)
    
    rmse = []
    for proportion in trainProportions:
        num = int(proportion*len(storeItemDF))
        train = storeItemDF[:num]
        test = storeItemDF[num:]
        
        prophet = Prophet()
        prophet.add_seasonality(name='yearly', period=365, fourier_order=10)
        prophet.fit(train)
        future = prophet.make_future_dataframe(periods=len(test))
        forecast = prophet.predict(future)
        rmse.append(np.sqrt(mean_squared_error(test['y'], forecast.yhat[-len(test):])))
    
    for root in rmse:
        for check in rmse:
            if abs(getPercentError(root, check)) > 0.2:
                return False
    return True 

''' get predictions in pandas dataframe '''
def getForecastPandas(storeNum, itemNum, numDays=30, totalInfo=False, printSummary=True):
    df = getDF(storeNum, itemNum)
    #testValue = testDF(storeNum, itemNum)
    prophet = Prophet()
    prophet.add_seasonality(name='yearly', period=365, fourier_order=10)
    prophet.fit(df)
    numDays = int(numDays)
    future = prophet.make_future_dataframe(periods=numDays)
    forecast = prophet.predict(future)

    forecast = forecast.rename(columns={'ds':'Date', 'yhat':'Predicted Sales'})
    forecast = forecast.set_index('Date')
    pred = forecast.iloc[-numDays:]
    
    if printSummary:   
        total = int(pred['Predicted Sales'].sum())
        margin = int((pred['yhat_upper'].sum() - pred['yhat_lower'].sum())/2)
        mySummary = 'The projected total sales for Item ' + str(itemNum) + ' at Store ' + str(storeNum) + ' for ' + str(numDays) + ' days is about ' + str(total) + ' with a margin of error of ' + str(margin)
    
    #if not testValue:
        #print('These predictions may not be completely accurate')
    pred['Predicted Sales'] = pred['Predicted Sales'].astype(int) 
    pred = pred.drop(columns=['multiplicative_terms', 'multiplicative_terms_lower', 'multiplicative_terms_upper' ])
    if totalInfo and printSummary:
        return pred, mySummary
    elif totalInfo and not printSummary:
        return pred
    elif not totalInfo and printSummary:
        return pred['Predicted Sales'], mySummary
    else:
        return pred['Predicted Sales']


''' get predictions in JSON format '''
def getForecastJSON(storeNum, itemNum, numDays=30, totalInfo=False, printSummary=True):
    if printSummary == True:
        df, summary = getForecastPandas(storeNum, itemNum, numDays, totalInfo=totalInfo, printSummary=printSummary)
        df.index = df.index.astype(str)
        salesJSON = df.to_json(orient='index')
        print(salesJSON)
        return salesJSON, summary
    else:
        df = getForecastPandas(storeNum, itemNum, numDays, totalInfo=totalInfo, printSummary=printSummary)
        df.index = df.index.astype(str)
        salesJSON = df.to_json(orient='index')
        return salesJSON

''' final function - choose dataframe or json for return value '''
def getForecast(storeNum, itemNum, numDays=30, totalInfo=True, printSummary=True, JSON=False):
    if JSON:
        return getForecastJSON(storeNum, itemNum, numDays, totalInfo, printSummary)
    else:
        if printSummary == True:
            df, summary = getForecastPandas(storeNum, itemNum, numDays, totalInfo, printSummary)
            df.index = df.index.strftime('%m/%d/%Y')
            for column in df.columns:
                df[column] = df[column]
            return df, summary
        else:
            df = getForecastPandas(storeNum, itemNum, numDays, totalInfo, printSummary)
            df.index = df.index.astype(str)
            return df






