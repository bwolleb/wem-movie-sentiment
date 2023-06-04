import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from PIL import Image



st.write("""
### F.U.C.K.C.E.D.R.I.C.
Film Understanding, Classification, Knowledge, and Comprehensive Emotion Detection, Revealing Intricate Connections
""")

path = 'E:\Technologie\Master\Webm\wem'

with open(f'{path}\movies.json',encoding="utf8") as f:
    data = json.load(f)


df = pd.DataFrame(data)


# Create a simple search engine

text_search = st.text_input("Search films by title", value="")

# Filter the dataframe using masks // lowering // de-accent the vowels
m1 = df["title"].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.contains(text_search.lower())
#m2 = df["year"].astype(str).str.contains(text_search)




#df_search = df[m1 | m2]

df_search = df[m1]

selected_movie = None
place_holders = []

# Show the results, if you have a text_search
if text_search:
    #st.write(df_search)
    N_cards_per_row = 3
    main_container = st.container()

    for n_row, row in df_search.reset_index().iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            placeholder = main_container.empty()
            place_holders.append(placeholder)
            placeholder.write("---")
            cols = main_container.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row % N_cards_per_row]:

            # Load the image from disk.
            image = Image.open(f'{path}\images\\{row["uuid"]}')
            # display the image
            image_placeholder = st.empty()
            place_holders.append(image_placeholder)
            image_placeholder.image(image, use_column_width=True)

            # titles and buttons
            markdown_placeholder = st.empty()
            place_holders.append(markdown_placeholder)
            markdown_placeholder.markdown(f"**{row['title']}**, {row['year']}")

            button_placeholder = st.empty()
            place_holders.append(button_placeholder)
            if button_placeholder.button(f"Select", key=row['uuid']):
                selected_movie = row["uuid"]

    if selected_movie is not None:
        main_container.empty()  # Clear the entire container, including columns
        for p in place_holders:  # Clear content of each placeholder
            p.empty()
        st.markdown(f"### Selected Movie: {selected_movie}")
        st.write("Display detailed information about the selected movie here.")
else:
    st.write(df)
