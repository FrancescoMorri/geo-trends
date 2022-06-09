import twint
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import folium as fl
from streamlit_folium import st_folium

def get_tweets(lat, lng, radius, N):
    c = twint.Config()
    c.Limit = N
    c.Popular_tweets = False
    c.Pandas = True
    c.Hide_output = True
    c.Geo = str(lat)+","+str(lng)+","+str(radius)+"km"

    twint.run.Search(c)
    return True


submitted = False

st.set_page_config(page_title="Geo-Trends", page_icon="earth_africa")

st.title("Geo-Trends")
st.caption("Choose a location on the map, specify a radius to search in and the number of tweets to scrape and wait for a graph of the most used hashtags in the area.")  


with st.form("Parameters"):
    m = fl.Map(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}.png',
                attr='Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC')
    m.add_child(fl.LatLngPopup())
    map = st_folium(m, height=350, width=700)
    
    tweets_n = st.slider("Number of tweets to search",10,5000,200,10)
    radius = st.slider("Radius around location to search (km)",1,10,2,1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.caption('You choose to search %d tweets, in a radius of %d km centered in (%.5f,%.5f)'%(tweets_n, radius, map['last_clicked']['lat'], map['last_clicked']['lng']))

if submitted:
    with st.spinner():
        get_tweets(map['last_clicked']['lat'], map['last_clicked']['lng'], radius,tweets_n)
    
    tweets_df = twint.storage.panda.Tweets_df

    if 'hashtags' in tweets_df:
        hashtag_text = ""
        for s in tweets_df['hashtags']:
            if len(s) > 0:
                for e in s:
                    hashtag_text += e + " "
        wordcloud = WordCloud(width = 2000, height = 1500, random_state=1, background_color='black',
                                 collocations=False, stopwords = STOPWORDS).generate(hashtag_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        ax.set_axis_off()
        st.pyplot(fig)
    else:
        st.error("There were not hashtags in the region searched. Try to increase the number of tweets and/or the radius.")


