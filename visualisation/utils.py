import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
import streamlit as st
from PIL import Image
from io import StringIO

tags = ["action", "addiction", "adolescence", "adoption", "adultery", "adventure", "alcohol", "alien", "amnesia", "animal", "animation", "anti hero", "apocalypse", "art", "artificial intelligence", "assassin", "bank", "betrayal", "biography", "business", "car", "casino", "celebrity", "chase", "children", "cinema", "comedy", "coming of age", "computer", "conspiracy", "crime", "cyberpunk", "dance", "dance", "dark comedy", "detective", "disaster", "documentary", "dog", "drama", "drug", "dystopia", "environment", "epic", "espionage", "family", "family drama", "fantasy", "fear", "film noir", "friendship", "future", "gambling", "gangster", "ghost", "gore", "heist", "high school", "historical", "horror", "human rights", "journey", "lgbt", "love", "martial arts", "magic", "mafia", "mental illness", "murder", "music", "musical", "mystery", "nature", "neo-noir", "paranormal", "period drama", "political satire", "politics", "post-apocalyptic", "psychological thriller", "racism", "religion", "romance", "romantic comedy", "satire", "sci-fi", "space", "sports", "spy", "superhero", "supernatural", "survival", "suspense", "terrorism", "thriller", "travel", "vampire", "war", "western", "zombie"]

def loadJson(path):
    f = open(path, encoding="utf8")
    data = json.load(f)
    f.close()
    return data

def eval0to100(res, poly):
    xs = [i / res * 100 for i in range(res + 1)]
    ys = [sum([val**i * poly[i] for i in range(len(poly))]) for val in xs]
    return xs, ys

def xy2pt(xs, ys):
    return [(xs[i], ys[i]) for i in range(len(xs))] 

signTemplates = {}
signTemplates["None"] = None
signTemplates["Selected movie"] = None
signTemplates["Globally positive"] = [-1, 0.02]
signTemplates["Globally negative"] = [1, -0.02]
signTemplates["Bad middle"] = [1, -0.08, 0.0008]
signTemplates["Good middle"] = [-1, 0.08, -0.0008]
signTemplates["Hope then despair"] = [0, 0.09, -0.0022, 1.23e-5]

def moving_average(x, width):
    return np.convolve(x, np.ones(width), 'valid') / width

def renderFigSVG(fig):
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    svg = imgdata.getvalue()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

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
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

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

    #st.pyplot(fig)
    renderFigSVG(fig)


def plot_sign(*signatures, colors=["grey", "blue", "red", "green", "orange", "purple"]):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(4, 2.5), constrained_layout=True)

    for i in range(len(signatures)):
        xs, ys = eval0to100(101, signatures[i])
        sns.lineplot(x=xs, y=ys, ax=ax, color=colors[i])

    ax.axhline(y=0, color="black", linestyle='--')
    ax.set_xlabel("Time (%)", fontsize=10)
    ax.set_ylabel("Sentiment", fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)

    st.pyplot(fig)

def func(x, poly):
    return [sum([val**i * poly[i] for i in range(len(poly))]) for val in x]

def selectMovie(uuid):
    st.session_state.selected_uuid = uuid
    st.session_state.last_selected = uuid

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
                plot_sign(selected_movie["signature"][2],row["signature"][2])

            # Load the image from disk.
            image = Image.open(os.path.join(path, "images", row["uuid"]))
            # display the image
            st.image(image, use_column_width=True)

            # titles and buttons
            st.markdown(f"**{row['title']}**, {row['year']}")

            # Display the tags
            style = "background-color: lightblue; padding: 2px; margin: 2px; display: inline-block; border-radius: 4px;"
            tags_str = ''.join([f'<span style="{style}">{tag.strip()}</span>' for tag in row['tags']])
            st.markdown(f"**Tags** : {tags_str}",unsafe_allow_html=True)

            st.button("Select", key=row['uuid'], on_click=selectMovie, args=[row['uuid']])


def matchSignature(data, refSignature, signIdx=2): # signIdx; 0=neg, 1=pos, 2=diff
    ids = []
    signatures = []
    for uuid, row in data.iterrows():
        ids.append(uuid)
        xs, ys = eval0to100(101, row["signature"][signIdx])
        signatures.append(ys)
    npIds = np.array(ids)
    npSign = np.array(signatures)

    xs, ys = eval0to100(101, refSignature)
    npRef = np.array(ys)
    mseComp = ((npSign - npRef)**2).mean(axis=1)
    sortedMseComp = mseComp.argsort()
    return list(npIds[sortedMseComp])

def searchMovie(data, title="", actors="", yearRange=None, ttrRange=None, tags=[], signature=None, maxNb=50):
    titleFilter = pd.Series(len(data) * [True], index=data["uuid"]) # Null mask
    if title != "":
        titleFilter = data["title"].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.contains(title.lower())

    dateFilter = pd.Series(len(data) * [True], index=data["uuid"]) # Null mask
    if yearRange is not None:
        dateFilter = data["year"].between(int(yearRange[0]), int(yearRange[1]))

    ttrFilter = pd.Series(len(data) * [True], index=data["uuid"]) # Null mask
    if ttrRange is not None:
        low = int(ttrRange[0]) / 100
        up = int(ttrRange[1]) / 100
        ttrFilter = data["ttr"].between(low, up)

    actorFilter = pd.Series(len(data) * [True], index=data["uuid"]) # Null mask
    if actors != "":
        actorList = actors.split(",")
        actorList = [a.strip() for a in actorList]
        actorFilter = data["actors"].apply(lambda actors: (sum([a.lower() in str.join(" ", actors).lower() for a in actorList]) == len(actorList)) if actors is not np.nan else False)

    tagFilter = pd.Series(len(data) * [True], index=data["uuid"]) # Null mask
    if len(tags) > 0:
        npTags = np.array(tags)
        tagFilter = data["tags"].apply(lambda tags: np.intersect1d(tags, npTags).size == len(npTags))

    result = data[titleFilter & dateFilter & ttrFilter & actorFilter & tagFilter]

    if signature != None:
        sortedBySignature = matchSignature(result, signature)
        result = result.reindex(sortedBySignature)

    return result.head(maxNb)
