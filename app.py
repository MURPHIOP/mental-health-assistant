import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
from textblob import TextBlob
from random import choice
import plotly.express as px

# Initialize DB
create_table()

# Page config
st.set_page_config(page_title="🧠 Mental Health Dashboard", layout="wide")

# Custom CSS for modern UI
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        color: #333333;
    }
    .title {
        font-size: 3em;
        font-weight: 700;
        text-align: center;
        color: #3f72af;
        margin-bottom: 0.2em;
    }
    .subheader {
        text-align: center;
        font-size: 1.3em;
        color: #5a5a5a;
        margin-bottom: 2em;
    }
    .log-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1em;
        margin-bottom: 1em;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .footer {
        margin-top: 3em;
        text-align: center;
        font-size: 0.9em;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🌈 Your Mental Health Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Track your emotions, reflect, and grow — one entry at a time.</div>", unsafe_allow_html=True)

# Daily Prompt
prompts = [
    "What made you feel proud today?",
    "Any moment that brought you peace recently?",
    "Is there something you're avoiding?",
    "What did you learn about yourself today?",
    "Write a note to your future self."
]
st.info(f"📌 Reflection Prompt: **{choice(prompts)}**")

# Text Input
user_input = st.text_area("✍️ Describe your current feelings:")

# Analyze Button
if st.button("Analyze Emotion"):
    if user_input.strip():
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

        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("## 🧠")
        with col2:
            st.markdown(f"### Emotion Detected: **{emotion}** ({score}%)")

        add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
    else:
        st.warning("Please describe your feelings before analyzing.")

# Mood History
st.markdown("---")
st.markdown("## 📅 Mood History & Suggestions")

logs = get_logs()
mood_tips = {
    "Happy": "Keep doing what makes you feel great! 😊",
    "Content": "Enjoy the calm — take time to reflect. 🧘",
    "Neutral": "Try journaling to understand your feelings better. 📓",
    "Sad": "Talk to someone you trust. You're not alone. 💬",
    "Depressed": "Reach out for support — you're valued. ❤️"
}

# Mood Chart
if logs:
    df_data = {"Date": [], "Mood": []}
    for log in logs:
        _, ts, emo, _ = log
        df_data["Date"].append(ts)
        df_data["Mood"].append(emo)
    fig = px.histogram(df_data, x="Date", color="Mood", title="Mood Trends Over Time",
                       color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)

for log in logs[::-1]:
    _, timestamp, emotion, text = log
    suggestion = mood_tips.get(emotion, "Take care of yourself today. 💖")

    st.markdown(f"""
        <div class='log-box'>
            <b>📅 Date:</b> {timestamp}<br>
            <b>😶 Emotion:</b> {emotion}<br>
            <b>📝 Entry:</b> {text}<br>
            <b>💡 Suggestion:</b> {suggestion}
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Shreyan Mitra | All rights reserved.</div>", unsafe_allow_html=True)



