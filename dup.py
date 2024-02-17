import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas_datareader as web
import yfinance as yf
# import time
import requests
from bs4 import BeautifulSoup
import streamlit as st
# from PIL import Image


st.set_page_config(
    page_title='Akash-Trader',
    layout='wide'
)


coll1,coll2,coll3=st.columns([2,3,1])
with coll1:
    st.title("Test Your Moving Average")

col1,col2=st.columns(2)

with col1:
    moving1= st.number_input("Enter Big moving Average")
    moving_window1=int(moving1)

col11,col12=st.columns(2)
with col11:
    moving2=st.number_input("Enter Small moving Average")
    moving_window2=int(moving2)
col21,col22=st.columns(2)

with col21:
    filtter=st.radio("Select To Filtter Stocks ",['All','Buy','Sell'])


lis=['ABBOTINDIA.NS', 'ACC.NS', 'ADANIENSOL.NS', 'ADANIGREEN.NS',
       'ADANIPORTS.NS', 'ALKEM.NS', 'AMBUJACEM.NS', 'ASIANPAINT.NS',
       'AUROPHARMA.NS', 'DMART.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS',
       'BAJFINANCE.NS', 'BAJAJHLDNG.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS',
       'BERGEPAINT.NS', 'BHARTIARTL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS',
       'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COLPAL.NS', 'CONCOR.NS',
       'DABUR.NS', 'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
       'GAIL.NS', 'GICRE.NS', 'GODREJCP.NS', 'GRASIM.NS', 'HAVELLS.NS',
       'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
       'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS',
       'HINDPETRO.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IGL.NS',
       'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INDIGO.NS',
       'IOC.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'LTIM.NS',
       'LUPIN.NS', 'M&M.NS', 'MARICO.NS', 'MARUTI.NS', 'MUTHOOTFIN.NS',
       'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OFSS.NS', 'ONGC.NS', 'PGHH.NS',
       'PETRONET.NS', 'PIDILITIND.NS', 'PEL.NS', 'PNB.NS', 'PFC.NS',
       'POWERGRID.NS', 'RELIANCE.NS','MOTHERSON.NS', 'SBIN.NS', 'SBICARD.NS',
       'SBILIFE.NS', 'SHREECEM.NS', 'SIEMENS.NS', 'SUNPHARMA.NS',
       'TATACONSUM.NS', 'TATAMOTORS.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS',
       'TORNTPHARM.NS', 'ULTRACEMCO.NS', 'UBL.NS', 'MCDOWELL-N.NS', 'UPL.NS',
       'WIPRO.NS', 'ZYDUSLIFE.NS']


di= pd.DataFrame()
if st.button("Refresh"):
    
    with st.spinner('Wait for few seconds.....'):
        
        dt=pd.DataFrame()
        url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&index=Nifty%20100&marketCapHigh=2000000&marketCapLow=0&page=0&size=100&sortBy=COMPANY_NAME&sortType=ASC'
        webpag=requests.get(url).text
        souppp=BeautifulSoup(webpag,'lxml')
        s=souppp.find_all('tr',class_="")
        Name=[]
        Price=[]
        change_price=[]
        t=0
        for i in s[1:98]:
            N=i.find_all('span',class_="st76SymbolName")
            P=(i.find_all('div',class_="st76CurrVal bodyBaseHeavy"))[0].text
            removequma=P.replace(",","")
            removerupee=removequma.replace("₹","")
            Price.append(float(removerupee))
        
            
            Name.append(N[0].text)
            
        
            
            w=i.find_all('div',class_="st76DivSec")
        
            target_div = w[0].find('div', {'class': 'bodySmallHeavy contentPositive'})
            if target_div:
                change=w[0].find_all('div',class_="bodySmallHeavy contentPositive")
                change_price.append(change[0].text)
        
            
            else:
                change=w[0].find_all('div',class_="bodySmallHeavy contentNegative")
                change_price.append(change[0].text)
        
        liss111=[]
        # liss222=[]
        for u in change_price:
            removeq=u.split('(', 1)[0]
            liss111.append(float(removeq))
            # removerup=u.split('(', 1)[1]
            # removeqq=removerup.split(')', 1)[0]
            # liss222.append(removeqq)
        dt['Name']=Name
        dt['Price']=Price
        dt['Change_price']=liss111
        
        trs=dt.T
        trs.columns = trs.iloc[0]
        trp = trs[1:2]
        # trp

        sl=trp.columns
        start_date = '2023-01-01'
        end_date = datetime.now()
        
        for i in lis:
            data = yf.download(i, start=start_date, end=end_date)
            di[sl[lis.index(i)]]=data["Close"] 
        
        # Concatinating both dataframe: yfin + grow
        result = pd.concat([di, trp], ignore_index=True)
        final_da=result.drop(len(result)-2)
        final_data=final_da.fillna(0)
        # st.dataframe(final_data)
        st.write(f"DataFrame Length: {len(final_data)}")
        pre_data=final_data[0:len(final_data)-2]
    
    
        oppo=[]
        for i in sl:
            # for pre_data calculating moving average
            pre_ma1=pre_data[i].rolling(moving_window1).mean()
            pre_f1=round(pre_ma1[len(pre_ma1)-1],2)
            pre_ma2 =pre_data[i].rolling(moving_window2).mean()
            pre_f2=round(pre_ma2[len(pre_ma2)-1],2)
        
            
            ma1 =final_data[i].rolling(moving_window1).mean()
            f1=round(ma1[len(ma1)],2)
            ma2 =final_data[i].rolling(moving_window2).mean()
            f2=round(ma2[len(ma2)],2)
            if (final_data.at[len(final_data),i]>=0) and (final_data.at[len(final_data),i]<=100):
                if (pre_f1 > pre_f2) and (f1 < f2)  :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2) :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
            elif (final_data.at[len(final_data),i]>=101) and (final_data.at[len(final_data),i]<=200):
                if (pre_f1 > pre_f2) and (f1 < f2)  :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2) :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
            elif (final_data.at[len(final_data),i]>=201) and (final_data.at[len(final_data),i]<=500):
                if (pre_f1 > pre_f2) and (f1 < f2) :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2) :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
        
            elif (final_data.at[len(final_data),i]>=501) and (final_data.at[len(final_data),i]<=1000):
                if (pre_f1 > pre_f2) and (f1 < f2) :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2) :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
        
            elif (final_data.at[len(final_data),i]>=1001) and (final_data.at[len(final_data),i]<=2000):
                if (pre_f1 > pre_f2) and (f1 < f2) :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2):
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
        
            elif (final_data.at[len(final_data),i]>=2001) and (final_data.at[len(final_data),i]<=5000):
                if (pre_f1 > pre_f2) and (f1 < f2)  :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2)  :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
        
            else :
                if (pre_f1 > pre_f2) and (f1 < f2) :
                    oppo.append("buy")
                elif (pre_f1 < pre_f2) and (f1 > f2) :
                    oppo.append("sell")
                else:
                    oppo.append("Wait for opportunity")
        dt["Recommended"]=oppo
        if filtter=="All":
            st.dataframe(dt)
            c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
            for n in range(len(dt)):
                o1=dt.iloc[n,0]
                o2=dt.iloc[n,1]
                o3=dt.iloc[n,2]
                if n<8:
                    with eval("c"+str(n+1)):
                        st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")









            
            
            comm1,comm2 = st.columns(2)
            dx=dt.sort_values(by='Change_price')
            dy=dt.sort_values(by='Change_price',ascending=False)
            for n in range(10):
                o1=dy.iloc[n,0]
                o2=dy.iloc[n,1]
                o3=dy.iloc[n,2]
                comm1.metric(label=o1, value=f"₹{o2}", delta=o3)
                o11=dx.iloc[n,0]
                o21=dx.iloc[n,1]
                o31=dx.iloc[n,2]
                comm2.metric(label=o11, value=f"₹{o21}", delta=o31)
        
        elif filtter=="Buy":
            stocks=dt[dt["Recommended"]=="buy"]
            com1, com2, com3,com4,com5 = st.columns(5)
            for n in range(len(stocks)):
                o1=stocks.iloc[n,0]
                o2=stocks.iloc[n,1]
                o3=stocks.iloc[n,2]
                eval("com"+str(n+1)).metric(label=f"₹{o2}", value=o1, delta=f"{o3}₹") 
        
            # st.dataframe(stocks, use_container_width=True)
        
        elif filtter=="Sell":
            stocks=dt[dt["Recommended"]=="sell"]
            com1, com2, com3,com4,com5 = st.columns(5)
            for n in range(len(stocks)):
                o1=stocks.iloc[n,0]
                o2=stocks.iloc[n,1]
                o3=stocks.iloc[n,2]
                eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
        
            # st.dataframe(stocks, use_container_width=True)
        else:
            stocks=dt[dt["Recommended"]=="Wait for opportunity"]
            # com1, com2, com3,com4,com5,com6 = st.columns(6)
            # for n in range(len(stocks)):
            #     o1=stocks.iloc[n,0]
            #     o2=stocks.iloc[n,1]
            #     o3=stocks.iloc[n,2]
            #     if n<15:
            #         with com1:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     elif n>=15 and n<30:
            #         with com2:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     elif n>=30 and n<45:
            #         with com3:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     elif n>=45 and n<60:
            #         with com4:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     elif n>=60 and n<75:
            #         with com5:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     elif n>=75 and n<90:
            #         with com6:
            #             st.metric(label=o1, value=f"₹{o2}", delta=o3)
            #     else:
            #         st.metric(label=o1, value=f"₹{o2}", delta=o3)

            st.dataframe(stocks, use_container_width=True)

    # st.success('Done!') 

    
    



