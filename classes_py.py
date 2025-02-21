import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf
import datetime as dt
import streamlit as st

class Blackscholes:
    def __init__(self,Strike,Stock,Time,RFR,Vol=None):
        ''' Basic Black Scholes calculator '''
        args = [Strike,Stock,Time,Vol,RFR]
        for i in args :
            if not isinstance(i,(int,float,dict)):
                raise Exception('Please check the types of the arguments, only float and int are accepted as valid arguments')
        else:   
            self.strike = Strike
            self.stock = Stock
            self.time = Time
            self.vol = Vol
            self.rf = RFR

    def calculate_d_option(self):
        pass

    def Calculate_price(self):
        pass


class call_option(Blackscholes):
    '''Call option class'''
    def __init__(self,Strike,Time,RFR,populate=False,Stock=None,ticker=None,Vol=None):
        if populate:
            self.strike = Strike
            self.time = Time
            self.ticker = ticker
            self.rf = RFR
            self.data = yf.download(self.ticker,start=dt.datetime.now() - dt.timedelta(365),end=dt.datetime.now())
            self.stock = np.round(self.data['Close'].iloc[-1,0],4)
            self.vol = np.round(self.data['Close'].pct_change().dropna().std().iloc[0],4)
        else:
            super().__init__(Strike, Stock, Time, RFR,Vol)
    
    def calculate_d_call(self):
        d1 = (np.log(self.stock / self.strike) + (self.rf + (self.vol ** 2) / 2) * self.time) / (self.vol * np.sqrt(self.time))
        d2 = d1 - self.vol * np.sqrt(self.time)
        return d1,d2
    
    def Calculate_price_call(self):
        d1 = self.calculate_d_call()[0]
        d2 = self.calculate_d_call()[1]
        price = self.stock * norm.cdf(d1) - ((self.strike * np.exp(-self.rf*self.time))*norm.cdf(d2))
        return price
    
class put_option(Blackscholes):
    '''Put option class'''
    def __init__(self,Strike,Time,RFR,populate=False,Stock=None,ticker=None,Vol=None):
        if populate:
            self.strike = Strike
            self.time = Time
            self.ticker = ticker
            self.rf = RFR
            self.data = yf.download(self.ticker,start=dt.datetime.now() - dt.timedelta(365),end=dt.datetime.now())
            self.stock = np.round(self.data['Close'].iloc[-1,0],4)
            self.vol = np.round(self.data['Close'].pct_change().dropna().std().iloc[0],4)
        else:
            super().__init__(Strike, Stock, Time, RFR,Vol)
    
    def calculate_d_put(self):
        d1 = (np.log(self.stock / self.strike) + (self.rf + (self.vol ** 2) / 2) * self.time) / (self.vol * np.sqrt(self.time))
        d2 = d1 - self.vol * np.sqrt(self.time)
        return d1,d2
    
    def Calculate_price_put(self):
        d1 = self.calculate_d_put()[0]
        d2 = self.calculate_d_put()[1]
        price = self.strike * np.exp(-self.rf * self.time) * norm.cdf(-d2) - self.stock * norm.cdf(-d1)
        return price
    
def selection_logic(model,fill,option):
    #Saved some if else clauses
    selection = {'Black Scholes':{'Autofill':{'Call':'bac','Put':'bap'},'Manual':{'Call':'bmc','Put':'bmp'}},'Heston':{'Autofill':{'Call':'hac','Put':'hap'},'Manual':{'Call':'hmc','Put':'hmp'}},'Stochastic':{'Autofill':{'Call':'sac','Put':'sap'},'Manual':{'Call':'smc','Put':'smp'}}}
    
    check = selection[model][fill][option]
    #Body logic for calculator
    if check.startswith('bm'):
        if check == 'bmc':
            value = call_option(Strike=strike,Stock=stock,Time=time,Vol=vol,RFR=rf).Calculate_price_call()
            st.write(f'The value for call option is {np.round(value,2)}')
        else:
            value = put_option(Strike=strike,Stock=stock,Time=time,Vol=vol,RFR=rf).Calculate_price_call()
            st.write(f'The value for put option is {np.round(value,2)}')
    elif check.startswith('ba'):
        if check == 'bac':
            value = call_option(Strike=strike,Time=time,RFR=rf,ticker=Ticker,populate=True)
            st.write(f'The value for call option is {np.round(value,2)}')
        else:
            value = put_option(Strike=strike,Time=time,RFR=rf,ticker=Ticker,populate=True)
            st.write(f'The value for put option is {np.round(value,2)}')
    elif check.startswith('ha'):
        pass
    elif check.startswith('hm'):
        pass
    elif check.startswith('sa'):
        pass
    else:
        pass

    return value