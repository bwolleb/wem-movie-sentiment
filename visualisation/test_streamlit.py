import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

searching = False

st.write("""
# My first app
Hello *world!*
""")

with open('E:\Technologie\Master\Webm\wem\movies.json',encoding="utf8") as f:
    data = json.load(f)


df = pd.DataFrame(data)
st.write(df)


# card style
selected_movie = None
# Show the results, if you have a text_search
if text_search:
    #st.write(df_search)
    N_cards_per_row = 3
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['title'].strip()} - {row['year']} ")
            # display the image
            #st.image(row['poster'], use_column_width=True)
            st.markdown(f"**{row['title']}**")
            if st.button(f"Select {row['title']}"):
                selected_movie = row["uuid"]
                text_search = ""
    if selected_movie != None:
        st.write("---")
        st.subheader(f"Selected Movie: {selected_movie}")
        st.write("Display detailed information about the selected movie here.")


# Create a simple search engine ************

text_search = st.text_input("Search videos by title or speaker", value="")

# Filter the dataframe using masks
m1 = df["title"].str.contains(text_search)
m2 = df["year"].astype(str).str.contains(text_search)

df_search = df[m1 | m2]

# Show the results, if you have a text_search
if text_search:
    st.write(df_search)


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data