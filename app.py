import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load anime data
animes_dict = pickle.load(open('model/animes_dict.pkl', 'rb'))
animes = pd.DataFrame(animes_dict)

# Load similarity data
@st.cache()
def recommend(anime):
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))

    index = animes[animes["Name"] == anime]["index"].values[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_summery = []
    recommended_anime_tags = []
    for i in distances[1:6]:
        recommended_anime_names.append(animes.iloc[i[0]].Name)
        recommended_anime_summery.append(animes.iloc[i[0]].Synopsis)
        recommended_anime_tags.append(animes.iloc[i[0]].Tags)

    return recommended_anime_names, recommended_anime_summery, recommended_anime_tags

# Apply dark mode using custom CSS
dark_mode_css = """
<style>
    body {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #dbabff;
    }
    select {
        background-color: #121212;
        color: #FFFFFF;
    }
    div.stSelectbox > div.stSelectboxLabel > label {
        color: #FFFFFF;
    }
    div.stSelectbox > div.stSelectboxControl {
        background-color: #121212;
        color: #FFFFFF;
    }
    div.stMarkdown > p {
        color: #FFFFFF;
    }
</style>
"""

# Streamlit app
st.markdown(dark_mode_css, unsafe_allow_html=True)

st.title('Recommend Anime')

selected_anime = st.selectbox(
    'Which anime did you like?',
    (animes['Name'].values))

if st.button('Recommend'):
    with st.spinner(text='In progress'):
        recommendations, summery, tags = recommend(selected_anime)
        st.success('Done')
        for i in range(5):
            st.markdown(f"<h5><strong>{i+1}) Title  : {recommendations[i]}</strong></h5>", unsafe_allow_html=True)
            st.write("Summary  : " + str(summery[i]))
            st.markdown(f"**Tags :  _{tags[i]}_**")