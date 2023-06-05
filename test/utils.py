
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

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


def get_best_matches_uuid(sign, ref="68a31a0cf30411edb451b8aeed79c0cc",n=4):
    def func(x, poly):
        return [sum([val**i * poly[i] for i in range(len(poly))]) for val in x]

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
    best4CompIds = [i for i in sortedMseComp[:n+1] if i != refId][:n] # Item itself is probably first
    return [ids[i] for i in best4CompIds]
    