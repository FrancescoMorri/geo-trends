import twint
import streamlit as st
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def get_tweets(location,radius,N):
    c = twint.Config()
    c.Limit = N
    c.Popular_tweets = False
    c.Pandas = True
    c.Hide_output = True
    c.Geo = str(location.latitude)+","+str(location.longitude)+","+str(radius)+"km"

    twint.run.Search(c)
    return True

geolocator = Nominatim(user_agent="thunder.vault00@gmail.com")

nation = ""
city = ""
street = ""
number = ""
submitted = False

st.title("Geo-Trends")
st.caption("Simply input a location specifying some of the following parameters to obtain an image with the most used hashtags in the tweets of the area")  

with st.form("Input Desired Location"):
    nation = st.text_input("Nation")
    city = st.text_input("City")
    street = st.text_input("Street")
    number = st.text_input("Number")
    tweets_n = st.slider("Number of tweets to search",10,5000,200,10)
    radius = st.slider("Radius around location to search (km)",1,10,2,1)
    loc = street + " " + number + " " + city + " " + nation
    location = geolocator.geocode(loc)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.subheader("Location")
        st.text(location.address)
        st.subheader("Coordinates")
        st.write(location.latitude, location.longitude)

if submitted:
    with st.spinner():
        get_tweets(location,radius,tweets_n)
    
    tweets_df = twint.storage.panda.Tweets_df

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
    st.balloons()

