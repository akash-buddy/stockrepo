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
    filtter=st.radio("Select To Filtter Stocks ",['All','Buy','Sell','Wait for opportunity'])


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
       'POWERGRID.NS', 'RELIANCE.NS', 'MOTHERSON.NS', 'SBIN.NS', 'SBICARD.NS',
       'SBILIFE.NS', 'SHREECEM.NS', 'SIEMENS.NS', 'SUNPHARMA.NS',
       'TATACONSUM.NS', 'TATAMOTORS.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS',
       'TORNTPHARM.NS', 'ULTRACEMCO.NS', 'UBL.NS', 'MCDOWELL-N.NS', 'UPL.NS',
       'WIPRO.NS', 'ZYDUSLIFE.NS']

sl=['Abbott India', 'ACC', 'Adani Energy Solut.', 'Adani Green Energy',
       'Adani Ports', 'Alkem Laboratories', 'Ambuja Cements', 'Asian Paints',
       'Aurobindo Pharma', 'Avenue Supermarts', 'Axis Bank', 'Bajaj Auto',
       'Bajaj Finance', 'Bajaj Holdings', 'Bandhan Bank', 'Bank of Baroda',
       'Berger Paints', 'Bharti Airtel', 'Biocon', 'Bosch', 'BPCL',
       'Britannia Industries', 'Cipla', 'Coal India', 'Colgate-Palmolive',
       'Container Corp', 'Dabur India', "Divi's Labs", 'DLF',
       "Dr Reddy's Labs", 'Eicher Motors', 'GAIL (India)', 'General Insurance',
       'Godrej Consumer', 'Grasim Industries', 'Havells India',
       'HCL Technologies', 'HDFC Asset Mgmt Co', 'HDFC Bank',
       'HDFC Life Insurance', 'Hero MotoCorp', 'Hindalco',
       'Hindustan Unilever', 'Hindustan Zinc', 'HPCL', 'ICICI Bank',
       'ICICI Lombard', 'ICICI Prudential', 'Indraprastha Gas', 'Indus Towers',
       'IndusInd Bank', 'Info Edge (India)', 'Infosys', 'Interglobe Aviation',
       'IOCL', 'ITC', 'JSW Steel', 'Kotak Mahindra Bank', 'L&T', 'LTIMindtree',
       'Lupin', 'Mahindra & Mahindra', 'Marico', 'Maruti Suzuki',
       'Muthoot Finance', 'Nestle India', 'NMDC', 'NTPC', 'OFSS', 'ONGC',
       'P&G', 'Petronet LNG', 'Pidilite Industries', 'Piramal Enterprises',
       'PNB', 'Power Finance Corp', 'Power Grid Corp', 'Reliance Industries',
       'Samvardhana Motherson', 'SBI', 'SBI Cards', 'SBI Life Insurance',
       'Shree Cement', 'Siemens', 'Sun Pharmaceutical', 'Tata Consumer',
       'Tata Motors', 'TCS', 'Tech Mahindra', 'Titan', 'Torrent Pharma',
       'UltraTech Cement', 'United Breweries', 'United Spirits', 'UPL',
       'Wipro', 'Zydus']



#fetcing data from yfin
# start_tim = time.time()
print("Expected time to download data ==> 1 Minute")
di= pd.DataFrame()


if st.button("Refresh"):
    start_date = '2023-01-01'
    end_date = datetime.now()
    
    for i in lis:
        data = yf.download(i, start=start_date, end=end_date)
        di[sl[lis.index(i)]]=data["Close"]                # yfinn data
    
    
    
    
    for i in range(1):
        lisss=[]
        url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&index=Nifty%20100&marketCapHigh=2000000&marketCapLow=0&page=0&size=100&sortBy=COMPANY_NAME&sortType=ASC'
        webpag=requests.get(url).text
        souppp=BeautifulSoup(webpag,'lxml')
        s=souppp.find_all('div',class_="st76CurrVal bodyBaseHeavy")
    
        for j in range(len(s)):
            d=s[j].text
            removequma=d.replace(",","")
            removerupee=removequma.replace("₹","")
            lisss.append(float(removerupee))
    
    #loading dataframe with Name and url-name
    gdf=pd.read_csv("nifty_100.csv")
    
    
    # New dataframe by appending real-time price 
    gdf['Price']=lisss
    
    # end_tim = time.time()
    # print('Duration: {}'.format(end_tim - start_tim))
    
    pd.set_option('display.max_rows', None)
    trs=gdf.T
    trs.columns = trs.iloc[0]
    trp = trs[2:]
    # trp
    
    
    # Concatinating both dataframe: yfin + grow
    result = pd.concat([di, trp], ignore_index=True)
    final_da=result.drop(len(result)-2)
    final_data=final_da.fillna(0)
    # st.dataframe(final_data)
    st.write(f"DataFrame Length: {len(final_data)}")









    oppo=[]
    for k in sl:
        ma1 =final_data[k].rolling(moving_window1).mean()
        f1=round(ma1[len(ma1)],2)
        ma2 =final_data[k].rolling(moving_window2).mean()
        f2=round(ma2[len(ma1)],2)
        if (final_data.at[len(final_data),k]>=0) and (final_data.at[len(final_data),k]<=100):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (3) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-3) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
        elif (final_data.at[len(final_data),k]>=101) and (final_data.at[len(final_data),k]<=200):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (3) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-3) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
    
        elif (final_data.at[len(final_data),k]>=201) and (final_data.at[len(final_data),k]<=500):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (3) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-3) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
    
        elif (final_data.at[len(final_data),k]>=501) and (final_data.at[len(final_data),k]<=1000):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (4) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-4) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
    
        elif (final_data.at[len(final_data),k]>=1001) and (final_data.at[len(final_data),k]<=2000):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (5) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-5) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
    
        elif (final_data.at[len(final_data),k]>=2001) and (final_data.at[len(final_data),k]<=5000):
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (10) ) :
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-10) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")
    
        else :
            if (f1 >= f2) and ((f1-f2) >= (0) and (f1-f2) <= (15) ) : 
                oppo.append("buy")
            elif (f1 <= f2) and ((f1-f2) >= (0) and (f1-f2) <= (-15) ) :
                oppo.append("sell")
            else:
                oppo.append("Wait for opportunity")


    gdf["Recommended"]=oppo
    if filtter=="All":
        st.dataframe(gdf)
    elif filtter=="Buy":
        stocks=gdf[gdf["Recommended"]=="buy"]
        st.dataframe(stocks, use_container_width=True)
    elif filtter=="Sell":
        stocks=gdf[gdf["Recommended"]=="sell"]
        st.dataframe(stocks, use_container_width=True)
    else:
        stocks=gdf[gdf["Recommended"]=="Wait for opportunity"]
        st.dataframe(stocks, use_container_width=True)
        
# print(" "*1)
# print(" 1 👈 For Buying stocks ")
# print(" 2 👈 For Selling stocks ")
# print(" 3 👈 For Opportunity stocks ")
# print(" "*1)
# print("#"*84)
# print(" "*1)
# cek=int(input("Choose number to see stocks -->"))
# print(" "*1)
# print("#"*84)
# print(" "*1)
# if cek==1:
#     stocks=gdf[gdf["Recommended"]=="buy"]
# elif cek==2:
#     stocks=gdf[gdf["Recommended"]=="sell"]
# else:
#     stocks=gdf[gdf["Recommended"]=="Wait for opportunity"]
    
    



