import pandas as pd
import streamlit as st 
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Vital Signs", page_icon=":bar_chart", layout="wide")
st.title(" :bar_chart: Vital Signs Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

#os.chdir(r'C:\Users\chira\OneDrive\Documents\decode\python')
df=pd.read_excel("Vital_Signs.xlsx")

## Creating Date filter
col1,col2=st.columns((2))
df['ADT']=pd.to_datetime(df['ADT'])

start_date=pd.to_datetime(df['ADT'].min())
end_date=pd.to_datetime(df['ADT'].max())

with col1:
    date1=pd.to_datetime(st.date_input("Start Date",start_date))

with col2:
    date2=pd.to_datetime(st.date_input("End Date",end_date))

df= df[(df['ADT']>=date1) & (df['ADT']<=date2)].copy()

## Creating Sidebar
st.sidebar.header('Choose Your Filter:')

##For Unique Subject ID
identifier=st.sidebar.multiselect('Pick Your Subject ID',df['USUBJID'].unique())
if not identifier:
    df2=df.copy()
else:
    df2=df[df['USUBJID'].isin(identifier)]

## For Treatment

treatment=st.sidebar.multiselect('Pick Treatment',df2['TRTA'].unique())
if not treatment:
    df3=df2.copy()
else:
    df3=df2[df2['TRTA'].isin(treatment)]

parameter=st.sidebar.multiselect('Pick parameter',df3['PARAM'].unique())
if not parameter:
    df4=df3.copy()
else:
    df4=df3[df3['PARAM'].isin(parameter)]

visit=st.sidebar.multiselect('Pick Visit',df4['VISIT'].unique())
if not visit:
    df5=df4.copy()
else:
    df5=df4[df4['VISIT'].isin(visit)]

# Filter the data based on Subject ID, Treatment, Parameter, visit

filtered_df = df5.copy()

# If only one parameter is selected, set title accordingly
parameter_title = "All Parameters"
if len(parameter) == 1:
    parameter_title = parameter[0]

category_df = filtered_df.groupby(by=["PARAM"], as_index=False)["AVAL"].mean()

with col1:
    st.subheader(f"Bar Chart for {parameter_title}")
    fig = px.bar(category_df, x="PARAM", y="AVAL", text=['{:,.2f}'.format(x) for x in category_df["AVAL"]],
                 template="simple_white", title=f"Average Value by Parameter ({parameter_title})")
    st.plotly_chart(fig, use_container_width=True, height=200)

new_category_df = filtered_df
with col2:
    st.subheader(f"Box Plot for {parameter_title}")
    fig = px.box(new_category_df, x='PARAM', y='AVAL', template="simple_white",
                 title=f"Distribution of Values by Parameter ({parameter_title})")
    st.plotly_chart(fig, use_container_width=True, height=200)

if len(parameter) == 1:
    category_df2 = filtered_df.groupby(by=['VISIT'], as_index=False)["AVAL"].mean()
    with col1:
        st.subheader(f'Bar Chart for Visits ({parameter_title})')
        fig = px.bar(category_df2, x='VISIT', y='AVAL', template='simple_white',
                     title=f'Average Value by Visit ({parameter_title})')
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f'Box Plot for Visits ({parameter_title})')
        fig = px.box(filtered_df, x='VISIT', y='AVAL', template='simple_white',
                     title=f'Distribution of Values by Visit ({parameter_title})')
        st.plotly_chart(fig, use_container_width=True, height=200)
