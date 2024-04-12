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
from PIL import Image


st.set_page_config(
    page_title='Akash',
    layout='wide'
)


col17,col27,col37=st.columns([3,1,3])
with col27:
    image=Image.open('bull.png')
    st.image(image,use_column_width=True)

coll1,coll2,coll3=st.columns([1.5,2,1])
with coll2:
    st.title("Try Your Moving Average")
    st.write(" ")
    

col1,col2=st.columns(2)

with col2:
    moving1= st.number_input("Enter Big moving Average")
    moving_window1=int(moving1)

    moving2=st.number_input("Enter Small moving Average")
    moving_window2=int(moving2)

    filtter=st.radio("Select To Filtter Stocks ",['All','Buy','Sell','Top Gainers','Top Losers'])

    option = st.selectbox('Sectors',("Nifty 100", "Banking" , "Energy" , "Agriculture", "Automobile"))

    butto=st.button("Refresh")
with col1:
    image=Image.open('what.jpg')
    edited=image.resize((3060,1900))
    st.image(edited,use_column_width=True)

st.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

if option=="Nifty 100":
    
    di= pd.DataFrame()
    if butto:
        
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
            df=pd.read_csv("2_March_saturday.csv")
            column_nam=list(df.columns)
            column_nam.pop(0)
            for col_name in column_nam:
                vr=column_nam.index(col_name)
                lio=[]
                for i in Name:
                    pp=df[df['Name']==i]
                    lio.append(pp.iloc[0,vr+1])
                dt[f'{col_name}']=lio
                
            trs=dt.T
            trs.columns = trs.iloc[0]
            trp = trs[1:len(trs)]
            # trp
            
            dp=pd.read_csv("nifty_100.csv")
            lis=[]
            linkk=[]
            for i in Name:
                ee=dp[dp['Name']==i]
                lis.append(ee.iloc[0,3])
                linkk.append(ee.iloc[0,2])
            
            sl=trp.columns
            
            start_date = '2023-06-01'
            # end_date = '2024-04-12'
            end_date = datetime.now()
            
            for i in lis:
                data = yf.download(i, start=start_date, end=end_date)
                di[sl[lis.index(i)]]=data["Close"] 
            di
            # Concatinating both dataframe: yfin + grow
            result = pd.concat([di, trp], ignore_index=True)
            # final_data=result.fillna(0)
            final_da=result.drop(len(result)-(len(trp)+1))
            final_data=final_da.fillna(0)
            st.dataframe(final_data)
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-len(trp)]
            # st.dataframe(pre_data)
    
            current_price=final_data[(len(final_data)-(len(trp))):len(final_data)-(len(trp)-1)]
            st.write(current_price)
            previous_price=final_data[(len(final_data)-(len(trp)+1)):len(final_data)-len(trp)]
            st.write(previous_price)
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            # dt['Change_price']=change_price
            dt.insert(2, 'Change_price', change_price)
            dt
            len(final_data)
            # final_data.at[len(final_data),]
            oppo=[]
            for i in sl:
                # for pre_data calculating moving average
                pre_ma1=pre_data[i].rolling(moving_window1).mean()
                pre_f1=round(pre_ma1[len(pre_ma1)-1],2)
                pre_ma2 =pre_data[i].rolling(moving_window2).mean()
                pre_f2=round(pre_ma2[len(pre_ma2)-1],2)
            
                
                ma1 =final_data[i].rolling(moving_window1).mean()
                f1=round(ma1[len(ma1)-1],2)
                ma2 =final_data[i].rolling(moving_window2).mean()
                f2=round(ma2[len(ma2)-1],2)
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
            dt["link"]=linkk
            dt["symbol"]=lis
        
            # st.write(dt)
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
    
            
            if filtter=="Top Gainers":
                dy=dt.sort_values(by='Change_price',ascending=False)
                com1, com2, com3 = st.columns(3)
                for n in range(9):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    simsim=dy.iloc[n,6]
                    grow_link=dy.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            

            if filtter=="Top Losers":
                dx=dt.sort_values(by='Change_price')
                com1, com2, com3 = st.columns(3)
                for n in range(9):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    simsim=dx.iloc[n,6]
                    grow_link=dx.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                      
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            


            
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                                    
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                    
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                                    
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                                    
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")

                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")

                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                                    
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

                    
            
            elif filtter=="Sell":
                stocks=dt[dt["Recommended"]=="sell"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                    
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                                    
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                    
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                                    
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                                    
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                    
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                                    
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')






            

    
# ..........................................................................................................................................................................................
# ........................................................................................................................................................................................
# ........................................................................................................................................................................................






if option=="Agriculture":
    
    di= pd.DataFrame()
    if butto:
        
        with st.spinner('Wait for few seconds.....'):
            
            df=pd.DataFrame()
            url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&industryIds=2,9,47,55,114&marketCapHigh=2000000&marketCapLow=0&page=0&size=110&sortBy=COMPANY_NAME&sortType=ASC'
            webpag=requests.get(url).text
            souppp=BeautifulSoup(webpag,'lxml')
            s=souppp.find_all('tr',class_="")
            Name=[]
            Price=[]
            change_price=[]
            t=0
            for i in s[2:]:
                N=i.find_all('span',class_="st76SymbolName")
                P=(i.find_all('div',class_="st76CurrVal bodyBaseHeavy"))[0].text
                removequma=P.replace(",","")
                removerupee=removequma.replace("₹","")
                Price.append(float(removerupee))
            
                
                Name.append(N[0].text)
            
            df['Name']=Name
            df['Price']=Price
            droped_df=df.drop_duplicates()
            dpp=pd.read_csv("Only_nse_agriculture.csv")
            dp=dpp.drop_duplicates()
            merdt=pd.merge(dp, droped_df, on='Name', how='left')
            lis=dp['Symbol'].tolist()
            linkk=dp['Link'].tolist()
    
            # dt= df[df['Name'].isin(dp['Name'])]
            dt=merdt[["Name","Price"]]
            Name_l=dt['Name'].tolist()
            
            df_s=pd.read_csv("2_March_saturday.csv")
            column_nam=list(df_s.columns)
            column_nam.pop(0)
            for col_name in column_nam:
                vr=column_nam.index(col_name)
                lio=[]
                for i in Name_l:
                    pp=df_s[df_s['Name']==i]
                    lio.append(pp.iloc[0,vr+1])
                dt[f'{col_name}']=lio
                
            trs=dt.T
            
            trs.columns = trs.iloc[0]
            trp = trs[1:len(trs)]
            # trp
            # li=dt['Name'].tolist()

            
            
            sl=trp.columns
            
            start_date = '2023-01-01'
            end_date = datetime.now()
            for i in lis:
                data = yf.download(i, start=start_date, end=end_date)
                di[sl[lis.index(i)]]=data["Close"] 
        
            # Concatinating both dataframe: yfin + grow
            result = pd.concat([di, trp], ignore_index=True)
            final_da=result.drop(len(result)-(len(trp)+1))
            final_data=final_da.fillna(0)
            # st.dataframe(final_data)
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-len(trp)]
            # st.dataframe(pre_data)
            
            current_price=final_data[(len(final_data)-(len(trp))):len(final_data)-(len(trp)-1)]
            previous_price=final_data[(len(final_data)-(len(trp)+1)):len(final_data)-len(trp)]
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            # dt['Change_price']=change_price
            dt.insert(2, 'Change_price', change_price)
            
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
            dt["Link"]=linkk
            dt["symbol"]=lis
    
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
    
            
            if filtter=="Top Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    grow_link=dy.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            if filtter=="Top Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    grow_link=dx.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3,com4,com5 = st.columns(5)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

                #     grow_link=stocks.iloc[n,5]
                #     if n<5:
                #         with eval("com"+str(n+1)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     elif n>=5 and n<10:
                #         with eval("com"+str(n-4)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
                # # st.dataframe(stocks, use_container_width=True)
            
            elif filtter=="Sell":
                stocks=dt[dt["Recommended"]=="sell"]
                com1, com2, com3,com4,com5 = st.columns(5)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

            #         grow_link=stocks.iloc[n,5]
            #         if n<5:
            #             with eval("com"+str(n+1)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         elif n>=5 and n<10:
            #             with eval("com"+str(n-4)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #         # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            
            #     # st.dataframe(stocks, use_container_width=True)
            # # else:
            # #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
            #     # st.dataframe(stocks, use_container_width=True) 


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



if option=="Automobile":
    
    di= pd.DataFrame()
    if butto:
        
        with st.spinner('Wait for few seconds.....'):
            
            df=pd.DataFrame()
            url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&industryIds=10,11,12,13,14,18,107,151,152&marketCapHigh=2000000&marketCapLow=0&page=0&size=150&sortBy=COMPANY_NAME&sortType=ASC'
            webpag=requests.get(url).text
            souppp=BeautifulSoup(webpag,'lxml')
            s=souppp.find_all('tr',class_="")
            Name=[]
            Price=[]
            change_price=[]
            t=0
            for i in s[2:]:
                N=i.find_all('span',class_="st76SymbolName")
                P=(i.find_all('div',class_="st76CurrVal bodyBaseHeavy"))[0].text
                removequma=P.replace(",","")
                removerupee=removequma.replace("₹","")
                Price.append(float(removerupee))
            
                
                Name.append(N[0].text)
            
            df['Name']=Name
            df['Price']=Price
            droped_df=df.drop_duplicates()
            dpp=pd.read_csv("Only_nse_automobile.csv")
            dp=dpp.drop_duplicates()
            merdt=pd.merge(dp, droped_df, on='Name', how='left')
            lis=dp['Symbol'].tolist()
            linkk=dp['Link'].tolist()
            # dt= df[df['Name'].isin(dp['Name'])]
            dt=merdt[["Name","Price"]]
            Name_l=dt['Name'].tolist()
            
            df_s=pd.read_csv("2_March_saturday.csv")
            column_nam=list(df_s.columns)
            column_nam.pop(0)
            for col_name in column_nam:
                vr=column_nam.index(col_name)
                lio=[]
                for i in Name_l:
                    pp=df_s[df_s['Name']==i]
                    lio.append(pp.iloc[0,vr+1])
                dt[f'{col_name}']=lio
                
            trs=dt.T
            
            trs.columns = trs.iloc[0]
            trp = trs[1:len(trs)]
            # trp
            li=dt['Name'].tolist()

            
            
            sl=trp.columns
            
            start_date = '2023-01-01'
            end_date = datetime.now()
            for i in lis:
                data = yf.download(i, start=start_date, end=end_date)
                di[sl[lis.index(i)]]=data["Close"] 
            
            # Concatinating both dataframe: yfin + grow
            result = pd.concat([di, trp], ignore_index=True)
            final_da=result.drop(len(result)-(len(trp)+1))
            final_data=final_da.fillna(0)
            # st.dataframe(final_data)
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-len(trp)]
            
            current_price=final_data[(len(final_data)-(len(trp))):len(final_data)-(len(trp)-1)]
            previous_price=final_data[(len(final_data)-(len(trp)+1)):len(final_data)-len(trp)]
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            # dt['Change_price']=change_price
            dt.insert(2, 'Change_price', change_price)
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
            dt["Link"]=linkk
            dt["symbol"]=lis
            
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
    
            
            if filtter=="Top Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    grow_link=dy.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            if filtter=="Top Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    grow_link=dx.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

                #     grow_link=stocks.iloc[n,5]
                #     if n<5:
                #         with eval("com"+str(n+1)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     elif n>=5 and n<10:
                #         with eval("com"+str(n-4)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
                # # st.dataframe(stocks, use_container_width=True)
            
            elif filtter=="Sell":
                stocks=dt[dt["Recommended"]=="sell"]
                com1, com2, com3,com4,com5 = st.columns(5)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

            #         grow_link=stocks.iloc[n,5]
            #         if n<5:
            #             with eval("com"+str(n+1)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         elif n>=5 and n<10:
            #             with eval("com"+str(n-4)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #         # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            
            #     # st.dataframe(stocks, use_container_width=True)
            # # else:
            # #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
            #     # st.dataframe(stocks, use_container_width=True) 


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if option=="Banking":
    
    di= pd.DataFrame()
    if butto:
        
        with st.spinner('Wait for few seconds.....'):
            
            df=pd.DataFrame()
            url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&industryIds=15,16&marketCapHigh=2000000&marketCapLow=0&page=0&size=50&sortBy=COMPANY_NAME&sortType=ASC'
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
            
            df['Name']=Name
            df['Price']=Price
            dpp=pd.read_csv("Only_nse_Banking.csv")
            dp=dpp.drop_duplicates()
            lis=dp['Symbol'].tolist()
            linkk=dp['Link'].tolist()
            dt= df[df['Name'].isin(dp['Name'])]
            dt=dt.drop_duplicates()
            Name_l=dt['Name'].tolist()
            
            df_s=pd.read_csv("2_March_saturday.csv")
            column_nam=list(df_s.columns)
            column_nam.pop(0)
            for col_name in column_nam:
                vr=column_nam.index(col_name)
                lio=[]
                for i in Name_l:
                    pp=df_s[df_s['Name']==i]
                    lio.append(pp.iloc[0,vr+1])
                dt[f'{col_name}']=lio
                
            trs=dt.T
            
            trs.columns = trs.iloc[0]
            trp = trs[1:len(trs)]
            # trp
            # trp
            li=dt['Name'].tolist()

            
            
            sl=trp.columns
            
            start_date = '2023-01-01'
            end_date = datetime.now()
            for i in lis:
                data = yf.download(i, start=start_date, end=end_date)
                di[sl[lis.index(i)]]=data["Close"] 
            
            # Concatinating both dataframe: yfin + grow
            result = pd.concat([di, trp], ignore_index=True)
            final_da=result.drop(len(result)-(len(trp)+1))
            final_data=final_da.fillna(0)
            # st.dataframe(final_data)
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-len(trp)]

            
            current_price=final_data[(len(final_data)-(len(trp))):len(final_data)-(len(trp)-1)]
            previous_price=final_data[(len(final_data)-(len(trp)+1)):len(final_data)-len(trp)]
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            # dt['Change_price']=change_price
            dt.insert(2, 'Change_price', change_price)
            
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
            dt["Link"]=linkk
            dt["symbol"]=lis
            
            if filtter=="All":
                # st.dataframe(dt)
                c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
                for n in range(len(dt)):
                    o1=dt.iloc[n,0]
                    o2=dt.iloc[n,1]
                    o3=dt.iloc[n,2]
                    # grow_link=dt.iloc[n,5]
                    if n<8:
                        with eval("c"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=8 and n<16:
                        with eval("c"+str(n-7)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=16 and n<24:
                        with eval("c"+str(n-15)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=24 and n<32:
                        with eval("c"+str(n-23)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=32 and n<40:
                        with eval("c"+str(n-31)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=40 and n<48:
                        with eval("c"+str(n-39)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=48 and n<56:
                        with eval("c"+str(n-47)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=56 and n<64:
                        with eval("c"+str(n-55)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=64 and n<72:
                        with eval("c"+str(n-63)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=72 and n<80:
                        with eval("c"+str(n-71)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=80 and n<88:
                        with eval("c"+str(n-79)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=88 and n<96:
                        with eval("c"+str(n-87)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=96 and n<100:
                        with eval("c"+str(n-95)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
    
            
            if filtter=="Top Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    grow_link=dy.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            if filtter=="Top Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    grow_link=dx.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

                #     grow_link=stocks.iloc[n,5]
                #     if n<5:
                #         with eval("com"+str(n+1)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     elif n>=5 and n<10:
                #         with eval("com"+str(n-4)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
                # # st.dataframe(stocks, use_container_width=True)
            
            elif filtter=="Sell":
                stocks=dt[dt["Recommended"]=="sell"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

            #         grow_link=stocks.iloc[n,5]
            #         if n<5:
            #             with eval("com"+str(n+1)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         elif n>=5 and n<10:
            #             with eval("com"+str(n-4)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            #         # st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #     # st.dataframe(stocks, use_container_width=True)
            # # else:
            # #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
            #     # st.dataframe(stocks, use_container_width=True) 

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if option=="Energy":
    
    di= pd.DataFrame()
    if butto:
        
        with st.spinner('Wait for few seconds.....'):
            
            df=pd.DataFrame()
            url=f'https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&industryIds=17,62,75,79,83,145,146&marketCapHigh=2000000&marketCapLow=0&page=0&size=110&sortBy=COMPANY_NAME&sortType=ASC'
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
            
            df['Name']=Name
            df['Price']=Price
            droped_df=df.drop_duplicates()
            dpp=pd.read_csv("Only_nse_Energy.csv")
            dp=dpp.drop_duplicates()
            merdt=pd.merge(dp, droped_df, on='Name', how='left')

            lis=dp['Symbol'].tolist()
            linkk=dp['Link'].tolist()
            # dt= df[df['Name'].isin(dp['Name'])]
            dt=merdt[["Name","Price"]]
            Name_l=dt['Name'].tolist()
            
            df_s=pd.read_csv("2_March_saturday.csv")
            column_nam=list(df_s.columns)
            column_nam.pop(0)
            for col_name in column_nam:
                vr=column_nam.index(col_name)
                lio=[]
                for i in Name_l:
                    pp=df_s[df_s['Name']==i]
                    lio.append(pp.iloc[0,vr+1])
                dt[f'{col_name}']=lio
                
            trs=dt.T
            
            trs.columns = trs.iloc[0]
            trp = trs[1:len(trs)]
            # trp
            # trp
            li=dt['Name'].tolist()

            
            
            sl=trp.columns
            
            start_date = '2023-01-01'
            end_date = datetime.now()
            for i in lis:
                data = yf.download(i, start=start_date, end=end_date)
                di[sl[lis.index(i)]]=data["Close"] 
            
            # Concatinating both dataframe: yfin + grow
            result = pd.concat([di, trp], ignore_index=True)
            final_da=result.drop(len(result)-(len(trp)+1))
            final_data=final_da.fillna(0)
            # st.dataframe(final_data)
            # st.write(f"DataFrame Length: {len(final_data)}")
            pre_data=final_data[0:len(final_data)-len(trp)]
            
            current_price=final_data[(len(final_data)-(len(trp))):len(final_data)-(len(trp)-1)]
            previous_price=final_data[(len(final_data)-(len(trp)+1)):len(final_data)-len(trp)]
            change_price=[]
            for i in range(len(sl)):
                change_p=current_price.iloc[0,i]-previous_price.iloc[0,i]
                change_price.append(round(change_p,2))
            # dt['Change_price']=change_price
            dt.insert(2, 'Change_price', change_price)
            
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
            dt["Link"]=linkk
            dt["symbol"]=lis
            
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
    
            
            if filtter=="Top Gainers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dy=dt.sort_values(by='Change_price',ascending=False)
                for n in range(10):
                    o1=dy.iloc[n,0]
                    o2=dy.iloc[n,1]
                    o3=dy.iloc[n,2]
                    grow_link=dy.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            if filtter=="Top Losers":
                comm1,comm2,comm3,comm4,comm5= st.columns(5)
                dx=dt.sort_values(by='Change_price')
                for n in range(10):
                    o1=dx.iloc[n,0]
                    o2=dx.iloc[n,1]
                    o3=dx.iloc[n,2]
                    grow_link=dx.iloc[n,5]
                    if n<5:
                        with eval("comm"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                    elif n>=5 and n<10:
                        with eval("comm"+str(n-4)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                
    
            elif filtter=="Buy":
                stocks=dt[dt["Recommended"]=="buy"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]
                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]

                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

                #     grow_link=stocks.iloc[n,5]
                #     if n<5:
                #         with eval("com"+str(n+1)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     elif n>=5 and n<10:
                #         with eval("com"+str(n-4)):
                #             st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                #             st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                #     # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            
                # # st.dataframe(stocks, use_container_width=True)
            
            elif filtter=="Sell":
                stocks=dt[dt["Recommended"]=="sell"]
                com1, com2, com3 = st.columns(3)
                for n in range(len(stocks)):
                    o1=stocks.iloc[n,0]
                    o2=stocks.iloc[n,1]
                    o3=stocks.iloc[n,2]

                    simsim=stocks.iloc[n,6]
                    grow_link=stocks.iloc[n,5]
                    if n<3:
                        with eval("com"+str(n+1)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=3 and n<6:
                        with eval("com"+str(n-2)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')
                    elif n>=6 and n<9:
                        with eval("com"+str(n-5)):
                            st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
                            st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
                            tab1, tab2,tab3= st.tabs(["Shareholding","Fundamental","News"])
                            urll=f'https://groww.in/stocks/{grow_link}'
                            webpag=requests.get(urll).text
                            souppp=BeautifulSoup(webpag,'lxml')
                            with tab1:
                                tett = souppp.find_all('div', class_="row col l12 shp76Row")
                                for inde_el in tett:
                                    holder= tett[tett.index(inde_el)].find_all('div', class_="bodyLarge")
                                    percentge = tett[tett.index(inde_el)].find_all('div', class_="shp76TextRight")
                                    st.write(f"{holder[0].text} --->> {percentge[0].text}")
                                
                            with tab2:
                                tex = souppp.find_all('div', class_="aboutCompany_summary__uP8fZ")
                                texx = souppp.find_all('td', class_="contentSecondary left-align bodyBase")
                                tex1 = souppp.find_all('td', class_="aboutCompany_tdValue__Ioaru right-align bodyLargeHeavy")
                                
                                # text = souppp.find_all('div', class_="col l12 stkP12Section")
                                # tex = text[1].find_all('div', class_="acs67Para")
                                about=tex[0].text
                                # texx = text[1].find_all('td', class_="acs67Head left-align bodyBase")
                                org=texx[0].text
                                fou=texx[1].text
                                MD=texx[2].text
                                # tex1 = text[1].find_all('td', class_="acs67Value right-align bodyLarge")
                                org_n=tex1[0].text
                                fou_n=tex1[1].text
                                MD_n=tex1[2].text
                                
                                st.write(about)
                                st.write(f"{org} --->> {org_n}")
                                st.write(f"{fou} --->> {fou_n}")
                                st.write(f"{MD} --->> {MD_n}")
                                
                                tb=souppp.find_all('table', class_="tb10Table col l12 ft785Table")
                                teb_left = tb[0].find_all('tr', class_="col l6 ft785RightSpace" )
                                teb_rigt = tb[0].find_all('tr', class_="col l6 ft785LeftSpace" )
                                for teb in teb_left:
                                    MC_l=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_l=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_l[0].text} ---->> {MC_vlue_l[0].text}")
                                for teb in teb_rigt:
                                    MC_r=teb.find_all('td', class_="ft785Head left-align contentSecondary bodyBase" )
                                    MC_vlue_r=teb.find_all('td', class_="ft785Value right-align contentPrimary bodyLargeHeavy" )
                                    st.write(f"{MC_r[0].text} ---->> {MC_vlue_r[0].text}")
                            with tab3:
                                url = f'https://finance.yahoo.com/quote/{simsim}?.tsrc=fin-srch'
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
                                webpage = requests.get(url, headers=headers).text
                                soup=BeautifulSoup(webpage,'lxml')
                                o=soup.find_all('div',class_="Py(14px) Pos(r)")
                                for i in o:
                                    wnew=i.find_all('a',class_="js-content-viewer")
                                    linnk=wnew[0]["href"]
                                    st.subheader(wnew[0].text)
                                    st.markdown(f'[Read Now](https://finance.yahoo.com{linnk})')

            #         grow_link=stocks.iloc[n,5]
            #         if n<5:
            #             with eval("com"+str(n+1)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         elif n>=5 and n<10:
            #             with eval("com"+str(n-4)):
            #                 st.metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹")
            #                 st.markdown(f'[Click here to Invest](https://groww.in/charts/stocks/{grow_link}?exchange=NSE)')
            #         # eval("com"+str(n+1)).metric(label=o1, value=f"₹{o2}", delta=f"{o3}₹") 
            
            #     # st.dataframe(stocks, use_container_width=True)
            # # else:
            # #     stocks=dt[dt["Recommended"]=="Wait for opportunity"]
            #     # st.dataframe(stocks, use_container_width=True) 










