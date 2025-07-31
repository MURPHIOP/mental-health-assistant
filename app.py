import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
from textblob import TextBlob
from random import choice

# Initialize DB
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

st.markdown("<div class='title'>🤔 Smart Mental Health Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>How are you feeling today? Type your thoughts below.</div>", unsafe_allow_html=True)

# Input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area("🧾 Describe your feelings:", value=st.session_state.user_input)

# Prompt
daily_prompts = [
    "What's one thing you're grateful for today?",
    "Did anything make you smile recently?",
    "What’s weighing on your mind?",
    "What small win did you have today?",
    "What do you need right now?"
]
st.info(f"💡 Daily Prompt: **{choice(daily_prompts)}**")

# Emotion keyword mapping
emotion_keywords = {
    "happy": "Happy",
    "joy": "Joyful",
    "excited": "Excited",
    "glad": "Glad",
    "calm": "Calm",
    "peaceful": "Calm",
    "relaxed": "Relaxed",
    "satisfied": "Content",
    "content": "Content",
    "hopeful": "Hopeful",
    "motivated": "Motivated",
    "confident": "Confident",
    "grateful": "Grateful",
    "loved": "Loved",
    "lonely": "Lonely",
    "bored": "Bored",
    "tired": "Tired",
    "sad": "Sad",
    "depressed": "Depressed",
    "upset": "Upset",
    "angry": "Angry",
    "furious": "Angry",
    "frustrated": "Frustrated",
    "anxious": "Anxious",
    "worried": "Worried",
    "nervous": "Nervous",
    "scared": "Fearful",
    "afraid": "Fearful",
    "guilty": "Guilty",
    "embarrassed": "Embarrassed",
    "jealous": "Jealous",
    "ashamed": "Ashamed",
    "shy": "Shy"
}

# Analyze
if st.button("🧠 Analyze Mood"):
    user_input = st.session_state.user_input.lower()
    if user_input.strip():
        matched_emotion = None
        for keyword in emotion_keywords:
            if keyword in user_input:
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

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 😊")
        with col2:
            st.markdown(f"### Detected Emotion: **{emotion}** ({score}%)")

        add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
    else:
        st.warning("Please enter something to analyze.")

# Logs
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
st.markdown("<div class='footer'>LAST MADE BY SHREYAN MITRA</div>", unsafe_allow_html=True)


