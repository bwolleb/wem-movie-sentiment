import math
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from PIL import Image
from utils import *
import sys
import os

st.set_page_config(layout="wide")


if 'selected_uuid' not in st.session_state: st.session_state['selected_uuid'] = None
if 'last_search' not in st.session_state: st.session_state['last_search'] = None
if 'last_selected' not in st.session_state: st.session_state['last_selected'] = None

#st.write("""
#### F.U.C.K.C.E.D.R.I.C.
#Film Understanding, Classification, Knowledge, and Comprehensive Emotion Detection, Revealing Intricate Connections
#""")

# get first argument of the command line
if len(sys.argv) > 1:
    path = sys.argv[1]
    path = path.replace("[", "").replace("]", "")
else:
    print("Please provide the path to the data folder as an argument")
    exit(1)

@st.cache_resource
def load_data():
    data = loadJson(os.path.join(path, "movies.json"))
    data_nlp = loadJson(os.path.join(path, "nlp.json"))
    df_nlp = pd.DataFrame(data_nlp).T
    df_data = pd.DataFrame(data)

    # set the uuid as index
    df_data.set_index('uuid', inplace=True)
    
    # join the two dataframes on the index and uuid
    df = df_data.join(df_nlp, how="inner")

    # add a column uuid from the index
    df['uuid'] = df.index

    # delete the rows where the signature is missing
    df = df[df['signature'].notna()]

    df = df[df['tags'].notna()]

    return df

df = load_data()

with st.sidebar:
    title = st.text_input("Search films by title", placeholder="title")
    actors = st.text_input("Search films by actor", placeholder="actors")
    start, end = min(df["year"]), max(df["year"])
    yearRange = st.select_slider("Year", options=[str(i) for i in range(start, end + 1)], value=(str(start), str(end)))
    start, end = int(100 * min(df["ttr"])), int(100 * max(df["ttr"])) + 1
    ttrRange = st.select_slider("TTR", options=[str(i) for i in range(start, end + 1)], value=(str(start), str(end)))
    tags = st.multiselect("Tags", tags)
    
    templates = [(k, signTemplates[k], i) for i, k in enumerate(signTemplates)]
    sign = st.selectbox("Typical signature", templates, format_func=lambda item: item[0])

    if sign[2] == 1 and st.session_state.last_selected is not None: # Current movie
        movie = df[df["uuid"] == st.session_state.last_selected].to_dict(orient="records")[0]
        sign = (sign[0], movie["signature"][2], sign[2])

    if sign[1] is not None:
        plot_sign(sign[1])

    if st.button("Apply", use_container_width=True):
        st.session_state.last_search = None
        st.session_state.selected_uuid = None

    searchTag = f"{title}/{actors}/{yearRange[0]}-{yearRange[1]}/{ttrRange[0]}-{ttrRange[1]}/{str.join('', tags)}/{sign[0]}"

if st.session_state.last_search != searchTag:
    st.session_state.last_search = searchTag
    st.session_state.selected_uuid = None
    df_search = searchMovie(df, title, actors, yearRange, ttrRange, tags, sign[1], 64)
    display_cards(df_search, path, N_cards_per_row=8)



elif st.session_state.selected_uuid is not None:
    selected_movie = df[df["uuid"] == st.session_state.selected_uuid].to_dict(orient="records")[0]
    analysis_data = loadJson(os.path.join(path, "analysis", selected_movie["uuid"] + ".json"))
    # dislay the title
    st.markdown(f"### Movie sentiment analysis : {selected_movie['title']}")

    
    cols = st.columns((10,3,40,4))


    with cols[0]:
        # display the image
        image = Image.open(os.path.join(path, "images", selected_movie["uuid"]))
        st.image(image, use_column_width=True)
        style = "background-color: lightblue; padding: 2px; margin: 2px; display: inline-block; border-radius: 4px;"
        tags_str = ''.join([f'<span style="{style}">{tag.strip()}</span>' for tag in selected_movie['tags']])
        st.markdown(f"**Tags** : {tags_str}",unsafe_allow_html=True)

    with cols[2]:

        tabs = st.tabs(["Informations", "Sentiment evolution", "Dramatic signature matching"])
        # Information tab
        with tabs[0]:
            # display the film title and year
            st.markdown(f" 📅 **Year** : {selected_movie['year']}")

            # display the duration from sub data (inexact but probably close)
            lastSub = analysis_data[-1][0]
            duration = "~"
            if lastSub >= 3600:
                duration += str(int(lastSub / 3600)) + "h "
                lastSub %= 3600
            duration += str(int(lastSub / 60)) + "mn"
            st.markdown(f" ⏱️ **Duration** : {duration}")

            # display the actors
            actors = "-"
            if selected_movie['actors'] is not np.nan:
                cleaned = [a for a in selected_movie['actors'] if a.strip() != ""]
                actors = str.join(", ", cleaned)
            st.markdown(f" 🎭 **Actors** : {actors}")

            # Display the tags
            style = "background-color: lightblue; padding: 2px; margin: 2px; display: inline-block; border-radius: 10px;"
            tags_str = ''.join([f'<span style="{style}">{tag.strip()}</span>' for tag in selected_movie['tags']])

            # Display the readability score
            st.markdown(f" 🤓 **Readability score** : {selected_movie['readability']}, **Flesh score** : {selected_movie['fre']}")

            # Display the Lexical variety score
            st.markdown(f" 📚 **Lexical variety score (TTR)** : {selected_movie['ttr']:.2f}")

            # display the plot
            with st.expander("**Plot of the movie**"):
                # test if the plot is a string
                if isinstance(selected_movie['plot'], str):
                    st.write(selected_movie['plot'].replace('$', '\\$'))
                else:
                    st.write("No plot available")

        # Sentiment analysis tab
        with tabs[1]:
            # display the plot showing the evolution of sentiment over time
            x, neg, pos, diff = computeNormAvg(analysis_data, 128)
            checks = st.columns(3)
            with checks[0]: display_pos = st.checkbox('positive',value=True)
            with checks[1]: display_neg = st.checkbox('negative',value=True)
            with checks[2]: display_diff = st.checkbox('delta',value=False)

            # radio button to select what to plot
            #plot_type = st.radio("Show", ["Positive & Negative", "Delta"], horizontal=True, label_visibility="hidden")
            #if plot_type == "Positive & Negative":
            #    display_pos = True
            #    display_neg = True
            #    display_diff = False
            #elif plot_type == "Delta":
            #    display_pos = False
            #    display_neg = False
            #    display_diff = True

            # prepare the data to be sent to the plot function according to the checkboxes
            dpos = pos if display_pos else None
            dneg = neg if display_neg else None
            ddiff = diff if display_diff else None

            # plot the sentiment evolution
            plot_sns(x, dneg, dpos, ddiff)

        # Dramatic signature matching tab
        with tabs[2]:
            # give a control to choose the number of matches to display
            n_matches = st.slider("Number of matchs", min_value=1, max_value=12, value=4)
            sortedBySignature = matchSignature(df, selected_movie["signature"][2])
            sortedBySignature.pop(sortedBySignature.index(selected_movie["uuid"]))
            matches = df.reindex(sortedBySignature[:n_matches])
            display_cards(matches, path, N_cards_per_row=4, display_plot=True, selected_movie=selected_movie)




if not st.session_state.last_search and st.session_state.selected_uuid is None:
    # for test purposes, display the entire dataframe
    #st.write(df)
    #st.write(df["signature"].to_dict())
    pass
