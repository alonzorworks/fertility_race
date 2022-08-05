import pandas as pd 
import streamlit as st 
import plotly.express as px 
import numpy as np
from streamlit_lottie import st_lottie
import requests


#NOTE Import Pictures 
def load_lottieurl(url):
    """If the lottie file does not display the image return nothing. This will prevent errors when trying to display the Lottie Files.
    Requires importing packages streamlit_lottie and requests"""
    r = requests.get(url)
    if r.status_code != 200:
        return None 
    return r.json()

def lottie_credit(credit):
    return st.markdown(f"<p style='text-align: center; color: gray;'>{credit}</p>", unsafe_allow_html=True)
    #return st.caption(credit)


st.set_page_config(page_title = "Fertility  By Race 1960-2013")

mother = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_bvynf4ow.json")



df = pd.read_csv("NHCS_fertility.csv")

df.replace("*", np.nan, inplace = True)

st.header("Fertility  By Race 1960-2013")

st_lottie(mother, width = 500)
lottie_credit("Covid and Mother and Baby by Joni Rodriguez")

st.write("This dataset comes from Data.World. This Data set was provided by the National Center for Health Statistics and is attributted to the Center for Disease Control per the Data.World website.")

st.write("Fertility and demographics is very important for various reasons. For this project the NHCS/CDC data will be presented and the viewer can make their own interpretation of how this may impact the future of the United States, if any.")

st.write("The dataset ranges from the year 1960-2013. There are four races that are recorded in the dataset. These races are White, Asian/Pacific Islander, American Indian/Alaska Native, and Black. The White race has the most recorded entries of any race. The other variables are Live Births, Birth Rate, and Fertility Rate.")


#df

# Fertility By Race 
st.subheader("Filter the data.")

col1, col2 = st.columns(2)
preg_mother = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_itSUNg.json")
mom_babe = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_hwnrae1k.json")

with col1:
    st_lottie(preg_mother)
    lottie_credit("Madre Embarazada By Gastón Solís LottieFiles")
with col2:
    st_lottie(mom_babe)
    lottie_credit("Mother and Her Son By DCE LottieFiles")


races = df["Race"].unique().tolist()
years = df["Year"].unique().tolist()


year_selection = st.slider("Choose Year Range:", 
min_value = min(years),
max_value = max(years),
value = (min(years),
max(years) )
)

race_multiselect = st.multiselect("Select Races to Observe", races,  default = races)

mask = (df["Year"].between(*year_selection)) & (df["Race"].isin(race_multiselect))

df[mask]

st.header("Line charts of all variables.")

all_variables = list(df.columns)
# Cutoff the variables not needed
all_variables = all_variables[2::]

#Gives a line chart for all of the pertinent variables
for i in all_variables:
    st.write(f"Chart of {i} Over Time - By Race")
    temp = px.line(df[mask], x = "Year", y = i, color = "Race", markers = True, width = 1000)
    st.plotly_chart(temp)


st.header("Bar Charts On The Basis of Race")
st.write("Note that there is some issues with this visual when applying filters.")
# Make a list of the pertinent variables 
df_sum = df[mask].groupby("Race", as_index= False ).sum()

live_births = px.bar(df_sum[mask] , x = "Race", y = "Live Births", color = "Race", width = 1000, text_auto = True)
st.plotly_chart(live_births)

st.subheader("Pie Chart Section")

for i in all_variables:
    st.write(f"Pie Chart of {i} - By Race")
    temp = px.pie(df[mask], values = i, names = "Race")
    st.plotly_chart(temp)