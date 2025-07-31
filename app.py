import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
from textblob import TextBlob
from random import choice
import pandas as pd
from collections import Counter
import plotly.express as px

# Initialize DB
create_table()

# Theme setup
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# Responsive Theme Switcher
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
        html, body, [class*="css"]  {{
            background-color: {bg_color} !important;
            color: {text_color};
        }}
        .title {{
            font-size: 2.5em;
            font-weight: bold;
            color: #4e73df;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subheader {{
            text-align: center;
            color: #6c757d;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}
        .log-box {{
            border-radius: 10px;
            padding: 1em;
            margin-bottom: 1em;
            background-color: {card_bg};
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.85em;
            color: #888;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 Smart Mental Health Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>How are you feeling today? Type your thoughts below or respond to a prompt.</div>", unsafe_allow_html=True)

# Text Input
user_input = st.text_area("🧾 Describe your feelings:", placeholder="Start typing your feelings here...")

# Daily Prompt
daily_prompts = [
    "What's one thing you're grateful for today?",
    "Did anything make you smile recently?",
    "What’s weighing on your mind?",
    "What small win did you have today?",
    "What do you need right now?"
]
st.info(f"💡 Prompt: **{choice(daily_prompts)}**")

# Emotion keyword mapping
emotion_keywords = {
    "happy": "Happy", "joy": "Joyful", "excited": "Excited", "glad": "Glad",
    "calm": "Calm", "peaceful": "Calm", "relaxed": "Relaxed", "satisfied": "Content",
    "content": "Content", "hopeful": "Hopeful", "motivated": "Motivated",
    "confident": "Confident", "grateful": "Grateful", "loved": "Loved",
    "lonely": "Lonely", "bored": "Bored", "tired": "Tired", "sad": "Sad",
    "depressed": "Depressed", "upset": "Upset", "angry": "Angry",
    "furious": "Angry", "frustrated": "Frustrated", "anxious": "Anxious",
    "worried": "Worried", "nervous": "Nervous", "scared": "Fearful",
    "afraid": "Fearful", "guilty": "Guilty", "embarrassed": "Embarrassed",
    "jealous": "Jealous", "ashamed": "Ashamed", "shy": "Shy"
}

# Analyze
if st.button("🔍 Analyze Mood"):
    user_input_lower = user_input.lower()
    if user_input_lower.strip():
        matched_emotion = None
        for keyword in emotion_keywords:
            if keyword in user_input_lower:
                matched_emotion = emotion_keywords[keyword]
                break

        if matched_emotion:
            emotion = matched_emotion
            score = 100.0
        else:
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

        st.success(f"**Detected Emotion:** {emotion} ({score}%)")
        add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
    else:
        st.warning("Please type something to analyze.")

# Mood Log
st.markdown("---")
st.subheader("📅 Mood History")
logs = get_logs()

if logs:
    for log in logs:
        _, timestamp, emotion, text = log
        st.markdown(f"""
            <div class='log-box'>
                <b>🗓️ {timestamp}</b> | <b>😶 Emotion:</b> {emotion}<br>
                <b>📝 Entry:</b> {text}
            </div>
        """, unsafe_allow_html=True)

    # Chart section
    df = pd.DataFrame(logs, columns=['id', 'date', 'emotion', 'entry'])
    df_count = df.groupby('date')['emotion'].apply(lambda x: Counter(x).most_common(1)[0][0]).reset_index()
    fig = px.line(df_count, x='date', y='emotion', title='Mood Over Time', markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No mood logs yet. Once you analyze your thoughts, they will appear here.")

# Footer
st.markdown("<div class='footer'>🚀 Built by Shreyan Mitra | Smart Mental Health Dashboard</div>", unsafe_allow_html=True)


