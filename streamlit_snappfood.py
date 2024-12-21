import streamlit as st
import statsmodels.api as sm
import plotly.express as px
import pandas as pd
import numpy as np 
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

#st.subheader("Region wise Sales")
#fig = px.bar(filtered_df, y= "amount", x = "dates")
#st.plotly_chart(fig,use_container_width=True)  

coll1, coll2 = st.columns((2))


st.subheader("Relationship between real price and amount")
fig1 = px.scatter(filtered_df, y = "amount", x= "real price",trendline='ols',log_x=True,log_y=True)
    
st.plotly_chart(fig1,use_container_width=True)



    
st.subheader("two factor regression : q1 = p  ")
X = np.log(filtered_df[["real price"]])
y =  np.log(filtered_df["amount"])
X = sm.add_constant(X) 
est = sm.OLS(y, X).fit() 

if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is not statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
st.write(est.summary())
   
    

    
results = px.get_trendline_results(fig1)


#st.write(results.px_fit_results.iloc[0].summary())

st.subheader("two factor regression : q1 = p + qt   (the all amounts sold is added to the equation)"  )
X = np.log(filtered_df[["real price","total of fruits in one month"]])
y =  np.log(filtered_df["amount"])
X = sm.add_constant(X) 
est = sm.OLS(y, X).fit() 

if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is not statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
st.write(est.summary())

column1,column2 = st.columns((2))
st.subheader("two factor regression : q1 = p + q' (the percentage of one fruite to total is added to the equation)")
X = np.log(filtered_df[["real price","percentage of one fruit"]])
y =  np.log(filtered_df["amount"])
X = sm.add_constant(X) 
est = sm.OLS(y, X).fit() 


if est.pvalues["real price"] <= 0.05:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
else:
    s = f"<p style='font-size:25px;'> {np.round(est.params["real price"],4)} is the sensitivity of price and it is not statistically large </p>"
    st.markdown(s, unsafe_allow_html=True)  
    

  

st.write(est.summary())

    
        
    
    


csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")
