import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))


if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\win\Desktop")
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


with col1:
    st.subheader("Relationship between real price and amount")
    fig = px.scatter(filtered_df, y = "amount", x= "real price",trendline='ols',log_x=True,log_y=True)
    
    st.plotly_chart(fig,use_container_width=True)


with col2:
    st.subheader("Region wise Sales")
    fig = px.bar(filtered_df, y= "amount", x = "dates")
    
    
    st.plotly_chart(fig,use_container_width=True)



csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")