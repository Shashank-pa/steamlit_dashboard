import streamlit as st
import os
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
os.chdir('C:\\Users\\Admin\\Desktop\\BS Project')
from classes_py import *


st.set_page_config(layout='wide')

st.title('Option Value Calculator',)

col1,col2 = st.columns(2)

#Inputs
with col1:
    risk_model = st.selectbox('Underlying risk engine:',options=['Black Scholes','Heston','Stochastic'])
    auto_fill = st.radio('Input',options=['Manual', 'Autofill'])
    if auto_fill == 'Manual':
        st.header('Risk settings')
        strike = st.number_input('Strike:', value=0.0, step=0.5)
        stock = st.number_input('Stock:', value=0.0, step=0.5)
        vol= st.number_input('Volatility (Annualised):', value=0.0, step=0.5)
        time = st.number_input('Time to maturity:', value=0.0, step=0.5)
        rf = st.number_input('Risk free rate (Country based):', value=0.0, step=0.5)
        radio2 = st.radio('Call or Put option',options=['Call','Put'])
    else:
        st.header('Risk settings - Autofill')
        ticker = st.text_input('Ticker:',placeholder='eg. INFY.NS')
        strike = st.number_input('Strike:', value=0.0, step=0.5)
        time = st.number_input('Time to maturity:', value=0.0, step=0.5)
        rf = st.number_input('Risk free rate (Country based):', value=0.0, step=0.5)
        radio2 = st.radio('Call or Put option',options=['Call','Put'])


#For Graphs
with col2:
    st.title('This area is for plots and stuff like this')
    select_col2 = st.selectbox(label='Graph setting',options=['Heatmap','Simulations'])
    if select_col2 == 'Heatmap':
        st.write('Coming soon')
    else:
        st.write('Coming soon')
        container = st.container(height=600,border=True,key='graphcol')
        with container:
            data = yf.download('AAPL',start=dt.datetime.now() - dt.timedelta(100),end=dt.datetime.now())
            data['Date'] = data.index.astype(str)
            st.write('Data downloaded')
            figure = px.line(data_frame=data,x=list(data.index),y=data.Close.AAPL,labels=['Time','Price'])
            st.plotly_chart(figure)


# def selection_logic(model,fill,option):
#     #Saved some if else clauses
#     selection = {'Black Scholes':{'Autofill':{'Call':'bac','Put':'bap'},'Manual':{'Call':'bmc','Put':'bmp'}},'Heston':{'Autofill':{'Call':'hac','Put':'hap'},'Manual':{'Call':'hmc','Put':'hmp'}},'Stochastic':{'Autofill':{'Call':'sac','Put':'sap'},'Manual':{'Call':'smc','Put':'smp'}}}
    
#     check = selection[model][fill][option]
#     st.write(check)
#     #Body logic for calculator
#     if check.startswith('bm'):
#         if check == 'bmc':
#             value = call_option(Strike=strike,Stock=stock,Time=time,Vol=vol,RFR=rf).Calculate_price_call()
#             st.write(f'The value for call option is {np.round(value,4)}')
#         else:
#             value = put_option(Strike=strike,Stock=stock,Time=time,Vol=vol,RFR=rf).Calculate_price_put()
#             st.write(f'The value for put option is {np.round(value,4)}')
#     elif check.startswith('ba'):
#         if check == 'bac':
#             value = call_option(Strike=strike,Time=time,RFR=rf,populate=True,ticker=ticker).Calculate_price_call()
#             st.write(f'The value for call option is {np.round(value,4)}')
#         else:
#             value = put_option(Strike=strike,Time=time,RFR=rf,populate=True,ticker=ticker).Calculate_price_put()
#             st.write(f'The value for put option is {np.round(value,4)}')
#     elif check.startswith('ha'):
#         pass
#     elif check.startswith('hm'):
#         pass
#     elif check.startswith('sa'):
#         pass
#     else:
#         pass

#     return value

##USE A DESIGN INSTEAD OF CREATING A COMPLEX LOGIC LIKE THIS

if st.button('Calculate',icon=':material/play_arrow:'):
    value = selection_logic(risk_model,auto_fill,radio2)