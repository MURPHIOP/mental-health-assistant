import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
from nrclex import NRCLex
from random import choice
import nltk
from nltk import data

# Ensure required NLTK data is available
try:
    data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize database
create_table()

# Theme setup
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

theme = st.selectbox("🌃 Theme", ['Light', 'Dark'], index=0 if st.session_state.theme == 'Light' else 1)
st.session_state.theme = theme

# Styling
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
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            color: #888;
        }}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='title'>🤔 Smart Mental Health Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>How are you feeling today? Type your thoughts below.</div>", unsafe_allow_html=True)

# Text input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area("🧾 Describe your feelings:", value=st.session_state.user_input)

# Daily prompt
daily_prompts = [
    "What's one thing you're grateful for today?",
    "Did anything make you smile recently?",
    "What’s weighing on your mind?",
    "What small win did you have today?",
    "What do you need right now?"
]
today_prompt = choice(daily_prompts)
st.info(f"💡 Daily Reflection Prompt: **{today_prompt}**")

# Analyze input
if st.button("🧠 Analyze Mood"):
    user_input = st.session_state.user_input.strip()
    if user_input:
        text_object = NRCLex(user_input)
        emotion_scores = text_object.raw_emotion_scores

        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            score = emotion_scores[dominant_emotion]
            total = sum(emotion_scores.values())
            confidence = round((score / total) * 100, 2)
        else:
            dominant_emotion = "Neutral"
            confidence = 0.0

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 😊")
        with col2:
            st.markdown(f"### Detected Emotion: **{dominant_emotion.capitalize()}** ({confidence}%)")

        add_log(date.today().strftime("%Y-%m-%d"), dominant_emotion, user_input)
    else:
        st.warning("Please enter your thoughts above.")

# Mood logs
st.markdown("---")
st.markdown("### 📅 Mood History")

logs = get_logs()
for log in logs:
    _, timestamp, emotion, text = log
    st.markdown(f"""
        <div class='log-box'>
            <b>🗓️ {timestamp}</b><br>
            <b>😶 Emotion:</b> <i>{emotion.capitalize()}</i><br>
            <b>📝 Entry:</b><br> {text}
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>LAST MADE BY SHREYAN MITRA</div>", unsafe_allow_html=True)
