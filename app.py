import re
import streamlit as st
from datetime import date
from db import create_table, add_log, get_logs
from random import choice

# ------------------- Extended Emotion Keywords -------------------
EMOTION_KEYWORDS = {
    "Happy": [
        "happy", "joy", "excited", "grateful", "pleased", "content", "delighted", "elated", "cheerful", "satisfied", "smile", "sunny"
    ],
    "Sad": [
        "sad", "unhappy", "down", "depressed", "blue", "crying", "gloomy", "heartbroken", "miserable", "upset", "tearful", "hopeless"
    ],
    "Angry": [
        "angry", "mad", "furious", "annoyed", "irritated", "enraged", "frustrated", "resentful", "rage", "fuming"
    ],
    "Fear": [
        "afraid", "scared", "fear", "terrified", "nervous", "panicked", "worried", "anxious", "insecure", "shaky", "helpless"
    ],
    "Surprise": [
        "surprised", "shocked", "amazed", "astonished", "startled", "speechless", "stunned", "unexpected"
    ],
    "Love": [
        "love", "loving", "caring", "affectionate", "passion", "fond", "heartwarming", "dear", "beloved", "intimate"
    ],
    "Anxious": [
        "anxious", "uneasy", "tense", "restless", "stressed", "nervous", "worried", "panic", "dread", "concerned"
    ],
    "Confident": [
        "confident", "strong", "capable", "proud", "bold", "assertive", "determined", "motivated"
    ],
    "Lonely": [
        "lonely", "isolated", "alone", "abandoned", "ignored", "neglected", "excluded"
    ]
}

def detect_emotion(text):
    text_lower = text.lower()
    matched_emotions = []

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', text_lower):
                matched_emotions.append(emotion)
                break  # Avoid double counting same emotion

    if not matched_emotions:
        return "Neutral"
    elif len(set(matched_emotions)) == 1:
        return matched_emotions[0]
    else:
        return "Mixed"
