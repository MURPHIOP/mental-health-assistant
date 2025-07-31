import streamlit as st
import plotly.express as px
from datetime import date
from db import create_table, add_log, get_logs
from streamlit_lottie import st_lottie
from textblob import TextBlob
import requests
import streamlit_authenticator as stauth

# ---------------- LOGIN CONFIG ---------------- #
config = {
    "credentials": {
        "usernames": {
            "shreyan": {
                "name": "Shreyan Mitra",
                "password": "$2b$12$KIXFZCnYVvQ2.0U0yU5a0uAhVYZvB2zJkm3SMxE3XpgVkPyxmw38K"  # pass123
            }
        }
    },
    "cookie": {
        "expiry_days": 30,
        "key": "auth",
        "name": "mentalhealth"
    },
    "preauthorized": {
        "emails": []
    }
}

authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'],
                                    config['cookie']['key'], config['cookie']['expiry_days'])

name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("❌ Incorrect username or password")
elif auth_status is None:
    st.warning("👤 Please enter your username and password")
elif auth_status:

    # ---------------- SETUP ---------------- #
    st.set_page_config(page_title="Mental Health Assistant", layout="wide")
    create_table()

    def load_lottie_url(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_json = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_tutvdkg0.json")

    st.markdown("""
        <style>
            body { font-family: 'Segoe UI', sans-serif; }
            .header { font-size: 2.5em; color: #3b82f6; font-weight: bold; }
            .subheader { font-size: 1.1em; color: #6b7280; margin-bottom: 20px; }
            .card {
                background: #ffffff;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------------- SIDEBAR ---------------- #
    mode = st.sidebar.radio("📋 Navigation", ["📝 Mood Journal", "📊 Mood Dashboard"])
    st.sidebar.markdown("---")
    st.sidebar.caption("🔒 Logged in as: " + name)
    st.sidebar.caption("👨‍💻 Made by Shreyan Mitra")

    # ---------------- EMOTION CLASSIFIER ---------------- #
    def classify_emotion(text):
        lower = text.lower()
        if any(word in lower for word in ["happy", "joy", "excited", "grateful", "love"]):
            return "Joy", "Keep smiling! 😊"
        elif any(word in lower for word in ["sad", "down", "cry", "depressed", "unhappy", "hopeless"]):
            return "Sadness", "It's okay to feel low. Talk to a friend or take a walk. 🌧️"
        elif any(word in lower for word in ["angry", "mad", "furious", "rage", "annoyed"]):
            return "Anger", "Try some deep breathing or time away. 🔥"
        elif any(word in lower for word in ["anxious", "worried", "nervous", "panic", "afraid"]):
            return "Fear", "Ground yourself. You're safe now. 🌱"
        elif any(word in lower for word in ["disgust", "gross", "nasty"]):
            return "Disgust", "Take a break from the situation. 🧼"
        elif any(word in lower for word in ["surprise", "shocked", "unexpected", "wow"]):
            return "Surprise", "Sometimes surprises can be good! 🎉"
        elif any(word in lower for word in ["bored", "meh", "tired", "lazy"]):
            return "Boredom", "Try something new or creative. 🎨"
        else:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.5:
                return "Joy", "That’s wonderful to hear! 🌟"
            elif polarity > 0:
                return "Content", "Nice and calm. Keep going. 😊"
            elif polarity < -0.5:
                return "Depressed", "Please take care. Talk to someone you trust. 💙"
            elif polarity < 0:
                return "Sadness", "Be kind to yourself today. 🌧️"
            else:
                return "Neutral", "Try journaling or a mindful break. 📝"

    # ---------------- JOURNAL PAGE ---------------- #
    if mode == "📝 Mood Journal":
        st.markdown("<div class='header'>🧠 Mental Health Assistant</div>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>Describe your current mood or situation.</div>", unsafe_allow_html=True)
        st_lottie(lottie_json, height=200)

        user_input = st.text_area("✍️ Your thoughts here:", placeholder="E.g., I'm feeling anxious and overwhelmed today...")

        if st.button("Analyze Mood"):
            if user_input.strip():
                emotion, tip = classify_emotion(user_input)
                st.success(f"### Detected Emotion: **{emotion}**")
                st.info(f"💡 Suggestion: *{tip}*")
                add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
            else:
                st.warning("Please enter your thoughts to analyze.")

    # ---------------- DASHBOARD ---------------- #
    elif mode == "📊 Mood Dashboard":
        st.markdown("<div class='header'>📈 Mood Tracker</div>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>View your emotion trends over time.</div>", unsafe_allow_html=True)

        logs = get_logs()

        if logs:
            dates, emotions, texts = zip(*[(log[1], log[2], log[3]) for log in logs])
            chart = px.histogram(x=dates, color=emotions, title="Mood History", labels={"x": "Date", "color": "Emotion"})
            st.plotly_chart(chart, use_container_width=True)

            st.markdown("### 💬 Mood Entries")
            for d, e, t in zip(dates, emotions, texts):
                _, tip = classify_emotion(t)
                st.markdown(f"""
                    <div class='card'>
                        <b>📅 {d}</b> — <b>{e}</b><br>
                        <i>{t}</i><br>
                        <small>💡 {tip}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You haven't logged any moods yet.")


