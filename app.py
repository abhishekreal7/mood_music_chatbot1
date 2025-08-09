import streamlit as st
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JAMENDO_CLIENT_ID = os.getenv("5c87b9ae")
jamendo_url = f"https://api.jamendo.com/v3.0/tracks/?client_id={JAMENDO_CLIENT_ID}&format=json&tags={mood}&limit=1"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="Mood Music Chatbot", page_icon="🎵")
st.title("🎵 Mood-Based Music Chatbot")
st.write("Tell me your mood, and I'll find you a matching song!")

# User input
user_input = st.text_input("You:", placeholder="Type your mood or feeling...")

if user_input:
    # Ask OpenAI to detect mood
    mood_prompt = f"Extract a single mood keyword from this sentence: '{user_input}'. Examples: happy, sad, romantic, energetic."
    mood_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": mood_prompt}]
    )
    mood = mood_response.choices[0].message.content.strip().lower()

    st.write(f"🎯 Detected mood: **{mood}**")

    # Fetch song from Jamendo
    jamendo_url = f"https://api.jamendo.com/v3.0/tracks/?client_id={JAMENDO_CLIENT_ID}&format=json&tags={mood}&limit=1"
    response = requests.get(jamendo_url)
    data = response.json()

    if data['results']:
        song = data['results'][0]
        st.write(f"🎵 **{song['name']}** by {song['artist_name']}")
        st.audio(song['audio'], format="audio/mp3")
        st.markdown(f"[Listen on Jamendo]({song['shareurl']})")
    else:
        st.warning("Sorry, I couldn't find a song for that mood.")
