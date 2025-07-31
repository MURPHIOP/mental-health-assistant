import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
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
st.markdown("<div class='subheader'>How are you feeling today? Speak or type your thoughts below.</div>", unsafe_allow_html=True)

# Text Area
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area("🧾 Describe your feelings (you can also use the microphone below):", value=st.session_state.user_input)

# Daily Prompt
daily_prompts = [
    "What's one thing you're grateful for today?",
    "Did anything make you smile recently?",
    "What’s weighing on your mind?",
    "What small win did you have today?",
    "What do you need right now?"
]
st.info(f"💡 Daily Prompt: **{choice(daily_prompts)}**")

# Voice Input (Web-based)
st.markdown("""
    <script>
        function startDictation() {
            if (window.hasOwnProperty('webkitSpeechRecognition')) {
                var recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = "en-US";
                recognition.start();
                recognition.onresult = function(e) {
                    var text = e.results[0][0].transcript;
                    window.parent.postMessage({ type: 'voice_input', text: text }, '*');
                    recognition.stop();
                };
                recognition.onerror = function(e) {
                    recognition.stop();
                    alert('Voice recognition error. Please try again.');
                };
            } else {
                alert("Your browser does not support Speech Recognition.");
            }
        }
    </script>
    <button onclick="startDictation()" style="padding: 10px 20px; font-size: 16px;">🎤 Speak</button>
""", unsafe_allow_html=True)

st.markdown("---")

# Listen to voice input result
st.markdown("""
    <script>
        window.addEventListener("message", (event) => {
            if (event.data?.type === "voice_input") {
                const textarea = window.parent.document.querySelector("textarea");
                if (textarea) {
                    textarea.value = event.data.text;
                    textarea.dispatchEvent(new Event("input", { bubbles: true }));
                }
            }
        });
    </script>
""", unsafe_allow_html=True)

# Emotion Detection
def detect_emotion(text):
    text = text.lower()
    emotion_keywords = {
        "Happy": ["joy", "excited", "grateful", "satisfied", "cheerful", "thankful", "content", "blessed"],
        "Sad": ["lonely", "disappointed", "unhappy", "regret", "gloomy", "tearful", "depressed"],
        "Angry": ["mad", "furious", "frustrated", "annoyed", "irritated", "rage"],
        "Fear": ["scared", "afraid", "anxious", "terrified", "nervous", "panic", "worried"],
        "Love": ["love", "loved", "caring", "affection", "compassion", "adore"],
        "Guilt": ["guilty", "remorse", "sorry", "ashamed"],
        "Surprised": ["surprised", "shocked", "amazed", "astonished", "speechless"],
        "Confused": ["confused", "uncertain", "doubt", "lost"],
        "Hopeful": ["hopeful", "optimistic", "confident", "bright future"],
        "Bored": ["bored", "uninterested", "tired", "dull"],
        "Neutral": []
    }

    match_count = {}
    for emotion, keywords in emotion_keywords.items():
        count = sum(word in text for word in keywords)
        if count:
            match_count[emotion] = count

    if match_count:
        detected = max(match_count, key=match_count.get)
        confidence = round((match_count[detected] / sum(match_count.values())) * 100, 2)
    else:
        detected = "Neutral"
        confidence = 0.0

    return detected, confidence

# Analyze
if st.button("🧠 Analyze Mood"):
    user_input = st.session_state.user_input
    if user_input.strip():
        emotion, confidence = detect_emotion(user_input)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### 😊")
        with col2:
            st.markdown(f"### Detected Emotion: **{emotion}** ({confidence}%)")

        add_log(date.today().strftime("%Y-%m-%d"), emotion, user_input)
    else:
        st.warning("Please enter or speak something to analyze.")

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


