# app.py
import streamlit as st
import speech_recognition as sr
from datetime import date
from db import create_table, add_log, get_logs
from textblob import TextBlob
from random import choice

# Initialize DB
create_table()

# Session Theme Setup
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

theme = st.selectbox("🌃 Theme", ['Light', 'Dark'], index=0 if st.session_state.theme == 'Light' else 1)
st.session_state.theme = theme

# CSS Styling
if theme == "Dark":
    bg_color = "#0e1117"
    text_color = "#ffffff"
    card_bg = "#1e1e1e"
else:
    bg_color = "#f7f9fc"
    text_color = "#000000"
    card_bg = "#ffffff"

st.set_page_config(page_title="Mental Health Assistant", layout="wide")
st.markdown(f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .title {{
            font-size: 3em;
            font-weight: bold;
            color: #4e73df;
            text-align: center;
        }}
        .subheader {{
            text-align: center;
            color: #6c757d;
            font-size: 1.2em;
            margin-bottom: 1em;
        }}
        .log-box {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1em;
            margin-bottom: 1em;
            background-color: {card_bg};
            color: {text_color};
        }}
        .footer {{
            text-align: center;
            margin-top: 3em;
            font-size: 0.9em;
            color: #888888;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🤔 Smart Mental Health Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>How are you feeling today? Speak or type below.</div>", unsafe_allow_html=True)

# Input Section
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area("Enter your feelings:", value=st.session_state.user_input)

if st.button("🎤 Use Voice Input"):
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Listening...")
            audio = recognizer.listen(source)
        spoken_text = recognizer.recognize_google(audio)
        st.session_state.user_input = spoken_text
        st.success(f"✅ You said: {spoken_text}")
    except Exception as e:
        st.warning("⚠️ Voice input may not work in this browser or cloud environment.")
        st.info(f"Error: {e}")

# Daily Prompt
daily_prompts = [
    "What's one thing you're grateful for today?",
    "Did anything make you smile recently?",
    "What’s weighing on your mind?",
    "What small win did you have today?",
    "What do you need right now?"
]
today_prompt = choice(daily_prompts)
st.info(f"💡 Daily Reflection Prompt: **{today_prompt}**")

# Analyze
if st.button("Analyze Mood"):
    user_input = st.session_state.user_input
    if user_input:
        analysis = TextBlob(user_input)
        polarity = analysis.sentiment.polarity

        if polarity > 0.5:
            emotion = "Happy"
        elif polarity > 0:
            emotion = "Content"
        elif polarity == 0:
            emotion = "Neutral"
        elif polarity > -0.5:
            emotion = "Sad"
        else:
            emotion = "Depressed"

        score = round(abs(polarity) * 100, 2)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 🧠")
        with col2:
            st.markdown(f"### Detected Emotion: **{emotion}** ({score}%)")

        add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
    else:
        st.warning("Please enter or speak your feelings.")

# Mood Logs
st.markdown("---")
st.markdown("### 📅 Mood History")
logs = get_logs()

for log in logs:
    _, timestamp, emotion, text = log
    st.markdown(f"""
        <div class='log-box'>
            <b>🗓️ {timestamp}</b><br>
            <b>😶 Emotion:</b> <i>{emotion}</i><br>
            <b>📝 Entry:</b><br> {text}
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>MADE BY SHREYAN MITRA</div>", unsafe_allow_html=True)
