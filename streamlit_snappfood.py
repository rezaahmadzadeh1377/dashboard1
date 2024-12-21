#importing the libraries 
import streamlit as st
import statsmodels.api as sm
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import os
import warnings
import seaborn as sns
warnings.filterwarnings('ignore')

# the title anfd the page name

st.set_page_config(page_title="fruitstore!!!", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Sample fruitstore")


#uploading data
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    #os.chdir(r"C:\Users\win\Desktop")
    df = pd.read_csv("file1.csv", encoding = "ISO-8859-1")

# Getting the min and max date 

df["dates"] = pd.to_datetime(df["dates"])
startDate = pd.to_datetime(df["dates"]).min()
endDate = pd.to_datetime(df["dates"]).max()

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["dates"] >= date1) & (df["dates"] <= date2)].copy()

#having a hierachial menue 

st.sidebar.header("Choose your filter: ")

fruit_type = st.sidebar.multiselect("Pick fruit type", df["fruit type"].unique())
if not fruit_type:
    df2 = df.copy()
else:
    df2 = df[df["fruit type"].isin(fruit_type)]

region = st.sidebar.multiselect("Pick your Region", df2["region"].unique())
if not region:
    df3 = df2.copy()
else:
    df3 = df2[df2["region"].isin(region)]


if not region and not fruit_type:
    filtered_df = df
elif not fruit_type:
    filtered_df = df[df["region"].isin(region)]
elif not region:
    filtered_df = df[df["fruit type"].isin(fruit_type)]
else:
    filtered_df = df3[df3["region"].isin(region) & df3["fruit type"].isin(fruit_type)]


#scattering price and amount 

st.subheader("Relationship between real price and amount")
fig1 = px.scatter(filtered_df, y = "amount", x= "real price",trendline='ols',log_x=True,log_y=True)
    
st.plotly_chart(fig1,use_container_width=True)


#information about regression 1
    
st.subheader("one factor regression : q1 = p  ")
X = np.log(filtered_df[["real price"]])
y =  np.log(filtered_df["amount"])
X = sm.add_constant(X) 
est = sm.OLS(y, X).fit() 

#showing the significance

if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is not statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
st.write(est.summary())
   
    
#regression 2 

st.subheader("two factor regression : q1 = p + qt   (the all amounts sold is added to the equation)"  )
X = np.log(filtered_df[["real price","total of fruits in one month"]])
y =  np.log(filtered_df["amount"])
X = sm.add_constant(X) 
est = sm.OLS(y, X).fit() 

#showing the significance 

if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is not statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
st.write(est.summary())



  


#scatrring real price and the percentage

st.subheader("Relationship between real price and amount and the share of fruits")
fig1 = px.scatter(filtered_df, y = "percentage of one fruit", x= "real price",trendline='ols',log_x=True,log_y=True)

 
X = np.log(filtered_df[["real price"]])
y =  np.log(filtered_df["percentage of one fruit"])
X = sm.add_constant(X) 

#regression and its significance

if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price to its share of total sale and it is statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price o its share of total sale and it is not statistically significant </p>"
    st.markdown(s, unsafe_allow_html=True)  
est = sm.OLS(y, X).fit()  
st.plotly_chart(fig1,use_container_width=True)


csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")
