import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json




path = 'E:\Technologie\Master\Webm\wem'

with open(f'{path}\\movies.json',encoding="utf8") as f:
    data = json.load(f)

with open(f'{path}\\nlp.json',encoding="utf8") as f:
    data_nlp = json.load(f)


df_data = pd.DataFrame(data)

df_nlp = pd.DataFrame(data_nlp).T

# set the uuid as index
df_data.set_index('uuid', inplace=True)
 
# join the two dataframes on the index and uuid
df = df_data.join(df_nlp, how="inner")

st.write(df)
