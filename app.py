import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from mood_model import detect_mood  # Import from mood_model.py

st.set_page_config(
    page_title="MoodScribe",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""<style>
    :root {
        --primary: #6A67CE;
        --secondary: #FF7BA9;
        --accent: #5FD9D9;
        --light: #F5F8FF;
        --dark: #2E3A59;
    }
    .title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
    }
    .subtitle {
        font-size: 1.3rem;
        color: var(--dark);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .box {
        background: linear-gradient(145deg, #ffffff, #f0f4ff);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(106, 103, 206, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 2rem;
        backdrop-filter: blur(4px);
    }
    .stButton>button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        display: block;
        margin: 1.5rem auto 0;
        box-shadow: 0 4px 20px rgba(106, 103, 206, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(106, 103, 206, 0.4);
    }
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 4px solid var(--primary);
    }
    .emoji-badge {
        font-size: 2.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .affirmation {
        background: linear-gradient(135deg, #e0f7fa, #f8bbd0);
        padding: 1.5rem;
        border-radius: 15px;
        font-style: italic;
        font-size: 1.2rem;
        border-left: 4px solid var(--secondary);
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        font-size: 0.9rem;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    textarea {
        border-radius: 15px !important;
        padding: 1rem !important;
    }
</style>""", unsafe_allow_html=True)

# --- Mood Data ---
MOOD_DATA = {
    "Happy": {
        "emoji": "😊",
        "color": "#FFD700",
        "songs": [
            "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
            "https://www.youtube.com/watch?v=y6Sxv-sUYtM",
            "https://www.youtube.com/watch?v=OPf0YbXqDm0",
            "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "https://www.youtube.com/watch?v=ru0K8uYEZWw",
            "https://www.youtube.com/watch?v=8j741TUIET0",
            "https://www.youtube.com/watch?v=PT2_F-1esPk",
            "https://www.youtube.com/watch?v=d-diB65scQU"
        ],
        "affirmations": [
            "Your joy is contagious! Keep shining your light ✨",
            "Celebrate this beautiful moment - you've earned it! 🌈",
            "Your positive energy creates ripples of goodness 🌊"
        ]
    },
    "Calm": {
        "emoji": "😌",
        "color": "#50C878",
        "songs": [
            "https://www.youtube.com/watch?v=7maJOI3QMu0",
            "https://www.youtube.com/watch?v=1ZYbU82GVz4"
        ],
        "affirmations": [
            "Peace flows through you like a gentle river 🌿",
            "In this stillness, you find your true strength 🍃",
            "You are centered and grounded in this moment 🌱"
        ]
    },
    "Motivated": {
        "emoji": "💪",
        "color": "#FF6B6B",
        "songs": [
            "https://www.youtube.com/watch?v=QtXby3twMmI",
            "https://www.youtube.com/watch?v=kX0vO4vlJuU"
        ],
        "affirmations": [
            "Your drive and passion move mountains! ⛰️",
            "Every step forward is a victory worth celebrating 🏆",
            "You have everything you need to succeed within you 🔥"
        ]
    },
    "Sad": {
        "emoji": "😢",
        "color": "#5C6BC0",
        "songs": [
            "https://www.youtube.com/watch?v=RB-RcX5DS5A",
            "https://www.youtube.com/watch?v=uelHwf8o7_U"
        ],
        "affirmations": [
            "It's okay to feel sad—healing starts with feeling 💧",
            "Your feelings are valid. You’re not alone 🌧️",
            "Every tear waters the seeds of strength 🌱"
        ]
    }
}

# --- Header ---
st.markdown('<div class="title">MoodScribe</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Write your mood. Hear your healing.</div>', unsafe_allow_html=True)

# --- Journal Entry ---
with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("📝 Reflect on Your Day")
    journal_text = st.text_area(
        "Describe how you're feeling today", 
        height=220, 
        placeholder="What's on your mind today? What emotions are you experiencing?",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button("🧠 Analyze Mood", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Result Section ---
if submitted:
    if not journal_text.strip():
        st.warning("Please share your thoughts before analyzing.")
        st.stop()

    with st.spinner("Reading between the lines..."):
        time.sleep(2)
        mood = detect_mood(journal_text)
        mood_data = MOOD_DATA.get(mood, MOOD_DATA["Calm"])
        song = random.choice(mood_data["songs"])
        affirmation = random.choice(mood_data["affirmations"])

        # Save to mood log
        mood_log = pd.DataFrame([[datetime.now(), journal_text, mood]], columns=["Timestamp", "Journal", "Mood"])
        try:
            existing = pd.read_csv("mood_log.csv")
            mood_log = pd.concat([existing, mood_log], ignore_index=True)
        except FileNotFoundError:
            pass
        mood_log.to_csv("mood_log.csv", index=False)

        st.balloons()
        st.markdown(f'<div class="emoji-badge pulse">{mood_data["emoji"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align: center; color: {mood_data["color"]}">{mood}</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 🎵 Music Recommendation")
            st.video(song)
            st.caption("Music tailored to enhance your current mood")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 💭 Your Affirmation")
            st.markdown(f'<div class="affirmation">{affirmation}</div>', unsafe_allow_html=True)
            st.markdown("### 📊 Mood Insights")
            st.progress(85 if mood == "Happy" else 65 if mood == "Calm" else 90 if mood == "Motivated" else 40)
            st.caption(f"Based on your writing, you're feeling {mood.lower()} today.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Agentic AI suggestions
        st.markdown("---")
        st.subheader("🤖 Suggestions for Well-being")
        if mood == "Sad":
            if st.button("🧘 Start a calming meditation"):
                st.video("https://www.youtube.com/watch?v=inpok4MKVLM")
            if st.button("📞 Talk to a mental health counselor"):
                st.write("[iCall India Mental Health Helpline](https://icallhelpline.org/)")
        elif mood == "Motivated":
            if st.button("🚀 Start a Pomodoro focus session"):
                st.video("https://www.youtube.com/watch?v=mNBmG24djoY")
        elif mood == "Happy":
            if st.button("🎉 Share your joy with someone"):
                st.write("Call or message someone you care about and share your moment!")

        st.markdown("---")
        st.subheader("🌱 Deepen Your Reflection")
        st.markdown("- What contributed most to how I'm feeling today?\n- How can I nurture this emotion tomorrow?\n- What does this mood reveal about my current needs?")

# --- Footer ---
st.markdown("---")
st.markdown('<div class="footer">🧠 Built with ❤️ for StartWell Hackathon 2025 | By Jatin Wig</div>', unsafe_allow_html=True)
