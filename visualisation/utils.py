
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from PIL import Image

@st.cache_data
def loadJson(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

def moving_average(x, width):
    return np.convolve(x, np.ones(width), 'valid') / width

def computeNormAvg(movie, avgWidth):
    neg = [entry[1] for entry in movie]
    pos = [entry[2] for entry in movie]
    avgNeg = moving_average(neg, avgWidth)
    avgPos = moving_average(pos, avgWidth)
    diff = []
    for i in range(len(avgPos)):
        diff.append(avgPos[i] - avgNeg[i])
    x = [entry[0] for entry in movie[:len(avgPos)]]
    factor = 100 / x[-1]
    normx = [r * factor for r in x]
    return normx, avgNeg, avgPos, diff

def plot_plt(x, neg=None, pos=None, diff=None, poly=None):
    fig, ax = plt.subplots(figsize=(5,2.5), constrained_layout=True)
    if neg is not None: ax.plot(x, neg, color="red", label="Negative Sentiment")
    if pos is not None: ax.plot(x, pos, color="green", label="Positive Sentiment")
    if diff is not None: ax.plot(x, diff, color="blue", label="Delta Sentiment")
    if poly is not None: ax.plot(x, poly, color="grey", label="Trend Line")

    ax.axhline(y=0, color="black", linestyle='--')
    ax.set_xlabel("Time (%)", fontsize=6)
    ax.set_ylabel("Sentiment", fontsize=6)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.legend(loc='upper left', fontsize=6)

    st.pyplot(fig,use_container_width=True)

def plot_st(x, neg=None, pos=None, diff=None, poly=None):
    data = {}
    if neg is not None: data['Negative Sentiment'] = neg
    if pos is not None: data['Positive Sentiment'] = pos
    if diff is not None: data['Delta Sentiment'] = diff
    if poly is not None: data['Trend Line'] = poly

    st.line_chart(data,use_container_width=True)

    #st.subheader("Sentiment Analysis")
    #st.write("This chart shows the sentiment analysis over time. The trend line represents the overall sentiment trend and the green and red lines represent the positive and negative sentiments respectively.")   

def plot_sns(x, neg=None, pos=None, diff=None, poly=None):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)

    if neg is not None:
        sns.lineplot(x=x, y=neg, ax=ax, color="red", label="Negative Sentiment")
    if pos is not None:
        sns.lineplot(x=x, y=pos, ax=ax, color="green", label="Positive Sentiment")
    if diff is not None:
        sns.lineplot(x=x, y=diff, ax=ax, color="blue", label="Delta Sentiment")
    if poly is not None:
        sns.lineplot(x=x, y=poly, ax=ax, color="grey", label="Trend Line")

    ax.axhline(y=0, color="black", linestyle='--')
    ax.set_xlabel("Time (%)", fontsize=16)
    ax.set_ylabel("Sentiment", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(loc='upper left', fontsize=14)


    st.pyplot(fig)


def plot_signature(signature_ref,signature):

    res = 100
    x = [i / res * 100 for i in range(res + 1)]
    comp_ref = func(x, signature_ref)
    comp_current = func(x, signature)


    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(4, 2.5), constrained_layout=True)

    sns.lineplot(x=x, y=comp_ref, ax=ax, color="red", label="Reference Signature")
    sns.lineplot(x=x, y=comp_current, ax=ax, color="blue", label="Signature")

    ax.axhline(y=0, color="black", linestyle='--')
    ax.set_xlabel("Time (%)", fontsize=10)
    ax.set_ylabel("Sentiment", fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.legend(loc='upper left', fontsize=10)

    st.pyplot(fig)

def func(x, poly):
    return [sum([val**i * poly[i] for i in range(len(poly))]) for val in x]

def get_best_matches_uuid(sign, ref="68a31a0cf30411edb451b8aeed79c0cc",n=4):

    ids = []
    signatures = []
    for uuid in sign:
        ids.append(uuid)
        signatures.append(sign[uuid][2])
    npSign = np.array(signatures)

    comp = []
    res = 100
    for poly in signatures:
        x = [i / res * 100 for i in range(res + 1)]
        comp.append(func(x, poly))
    npComp = np.array(comp)


    refId = ids.index(ref)
    refDiffComp = np.array(comp[refId])
    mseComp = ((npComp - refDiffComp)**2).mean(axis=1)
    sortedMseComp = mseComp.argsort()
    best4CompIds = [i for i in sortedMseComp[:n+1] if i != refId]
    return [ids[i] for i in best4CompIds]
    
def display_cards(df,path,N_cards_per_row = 8,display_plot=False,selected_movie=None):

    for n_row, row in df.reset_index().iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            if not display_plot:
                st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row % N_cards_per_row]:

            if display_plot and selected_movie is not None:
                # analysis_data = loadJson(f'{path}\\analysis\{row["uuid"]}.json')
                # x, neg, pos, diff = computeNormAvg(analysis_data, 128)
                plot_signature(selected_movie["signature"][2],row["signature"][2])

            # Load the image from disk.
            image = Image.open(f'{path}\images\\{row["uuid"]}')
            # display the image
            st.image(image, use_column_width=True)

            # titles and buttons
            st.markdown(f"**{row['title']}**, {row['year']}")

            # Display the tags
            style = "background-color: lightblue; padding: 2px; margin: 2px; display: inline-block; border-radius: 10px;"
            tags_str = ''.join([f'<span style="{style}">{tag.strip()}</span>' for tag in row['tags']])
            st.markdown(f"**Tags** : {tags_str}",unsafe_allow_html=True)

            if st.button(f"Select", key=row['uuid']):
                st.session_state.selected_uuid = row["uuid"]
                st.experimental_rerun()
    return