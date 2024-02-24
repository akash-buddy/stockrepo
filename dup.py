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

# tab1, tab2, tab3 = st.tabs(["Nifty 100", "Agriculture", "Automobile"])

# with tab1:

coll1,coll2,coll3=st.columns([3,2,1])
with coll1:
    st.title("Try Your Moving Average")

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
    filtter=st.radio("Select To Filtter Stocks ",['All','Buy','Sell','Top-10 Gainers','Top-10 Losers'])
col23,col24=st.columns(2) 
with col21:
    option = st.selectbox('Sectors',("Nifty 100", "Agriculture", "Automobile"))


if option=="Nifty 100":
    
    
    # lis=['ABBOTINDIA.NS', 'ACC.NS', 'ADANIENSOL.NS', 'ADANIGREEN.NS',
    #        'ADANIPORTS.NS', 'ALKEM.NS', 'AMBUJACEM.NS', 'ASIANPAINT.NS',
    #        'AUROPHARMA.NS', 'DMART.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS',
    #        'BAJFINANCE.NS', 'BAJAJHLDNG.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS',
    #        'BERGEPAINT.NS', 'BHARTIARTL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS',
    #        'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COLPAL.NS', 'CONCOR.NS',
    #        'DABUR.NS', 'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
    #        'GAIL.NS', 'GICRE.NS', 'GODREJCP.NS', 'GRASIM.NS', 'HAVELLS.NS',
    #        'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    #        'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS',
    #        'HINDPETRO.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IGL.NS',
    #        'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INDIGO.NS',
    #        'IOC.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'LTIM.NS',
    #        'LUPIN.NS', 'M&M.NS', 'MARICO.NS', 'MARUTI.NS', 'MUTHOOTFIN.NS',
    #        'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OFSS.NS', 'ONGC.NS', 'PGHH.NS',
    #        'PETRONET.NS', 'PIDILITIND.NS', 'PEL.NS', 'PNB.NS', 'PFC.NS',
    #        'POWERGRID.NS', 'RELIANCE.NS','MOTHERSON.NS', 'SBIN.NS', 'SBICARD.NS',
    #        'SBILIFE.NS', 'SHREECEM.NS', 'SIEMENS.NS', 'SUNPHARMA.NS',
    #        'TATACONSUM.NS', 'TATAMOTORS.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS',
    #        'TORNTPHARM.NS', 'ULTRACEMCO.NS', 'UBL.NS', 'MCDOWELL-N.NS', 'UPL.NS',
    #        'WIPRO.NS', 'ZYDUSLIFE.NS']
    # st.write(lis)
    
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
            for i in s[1:]:
                N=i.find_all('span',class_="st76SymbolName")
                P=(i.find_all('div',class_="st76CurrVal bodyBaseHeavy"))[0].text
                removequma=P.replace(",","")
                removerupee=removequma.replace("₹","")
                Price.append(float(removerupee))
            
                
                Name.append(N[0].text)
    
            dt['Name']=Name
            dt['Price']=Price        
            trs=dt.T
            trs.columns = trs.iloc[0]
            trp = trs[1:2]
            # trp
            
            dp=pd.read_csv("nifty_100.csv")
            lis=[]
            for i in Name:
                ee=dp[dp['Name']==i]
                lis.append(ee.iloc[0,3])
            
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
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-2]
    
            current_price=final_data[(len(final_data)-1):len(final_data)]
            previous_price=final_data[(len(final_data)-2):len(final_data)-1]
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            dt['Change_price']=change_price
            
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
                # st.dataframe(dt)
                c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
                for n in range(len(dt)):
                    o1=dt.iloc[n,0]
                    o2=dt.iloc[n,1]
                    o3=dt.iloc[n,2]
                    if n<8:
                        with eval("c"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=8 and n<16:
                        with eval("c"+str(n-7)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=16 and n<24:
                        with eval("c"+str(n-15)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=24 and n<32:
                        with eval("c"+str(n-23)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=32 and n<40:
                        with eval("c"+str(n-31)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=40 and n<48:
                        with eval("c"+str(n-39)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=48 and n<56:
                        with eval("c"+str(n-47)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=56 and n<64:
                        with eval("c"+str(n-55)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=64 and n<72:
                        with eval("c"+str(n-63)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=72 and n<80:
                        with eval("c"+str(n-71)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=80 and n<88:
                        with eval("c"+str(n-79)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=88 and n<96:
                        with eval("c"+str(n-87)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=96 and n<100:
                        with eval("c"+str(n-95)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
    
            
            if filtter=="Top-10 Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            if filtter=="Top-10 Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3,com4,com5 = st.columns(5)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
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
            # else:
            #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
                # st.dataframe(stocks, use_container_width=True) 

    
# ..........................................................................................................................................................................................
# ........................................................................................................................................................................................
# ........................................................................................................................................................................................

if option=="Agriculture":
    
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
    
            dt['Name']=Name
            dt['Price']=Price        
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
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-2]
    
            current_price=final_data[(len(final_data)-1):len(final_data)]
            previous_price=final_data[(len(final_data)-2):len(final_data)-1]
            change_price=[]
            for i in range(97):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            dt['Change_price']=change_price
            
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
                # st.dataframe(dt)
                c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
                for n in range(len(dt)):
                    o1=dt.iloc[n,0]
                    o2=dt.iloc[n,1]
                    o3=dt.iloc[n,2]
                    if n<8:
                        with eval("c"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=8 and n<16:
                        with eval("c"+str(n-7)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=16 and n<24:
                        with eval("c"+str(n-15)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=24 and n<32:
                        with eval("c"+str(n-23)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=32 and n<40:
                        with eval("c"+str(n-31)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=40 and n<48:
                        with eval("c"+str(n-39)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=48 and n<56:
                        with eval("c"+str(n-47)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=56 and n<64:
                        with eval("c"+str(n-55)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=64 and n<72:
                        with eval("c"+str(n-63)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=72 and n<80:
                        with eval("c"+str(n-71)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=80 and n<88:
                        with eval("c"+str(n-79)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=88 and n<96:
                        with eval("c"+str(n-87)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=96 and n<100:
                        with eval("c"+str(n-95)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
    
            
            if filtter=="Top-10 Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            if filtter=="Top-10 Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3,com4,com5 = st.columns(5)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    if n<5:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    elif n>=5 and n<10:
                        with eval("com"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                    # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
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
            # else:
            #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
                # st.dataframe(stocks, use_container_width=True) 



