import twint
import streamlit as st
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

geolocator = Nominatim(user_agent="thunder.vault00@gmail.com")

nation = ""
city = ""
street = ""
number = ""
submitted = False

st.title("Location Trends")

with st.form("Input Location"):
    nation = st.text_input("Nation")
    city = st.text_input("City")
    street = st.text_input("Street")
    number = st.text_input("Number")

    submitted = st.form_submit_button("Submit")
    if submitted:
        loc = street + " " + number + " " + city + " " + nation
        location = geolocator.geocode(loc)
        st.subheader("Location")
        st.text(location.address)
        st.subheader("Coordinates")
        st.write(location.latitude, location.longitude)

if submitted:
    c = twint.Config()
    c.Limit = 1000
    c.Popular_tweets = False
    c.Pandas = True
    c.Hide_output = True
    c.Geo = str(location.latitude)+","+str(location.longitude)+",2km"

    twint.run.Search(c)

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
    
else:
    st.spinner("Waiting...")