import os

import streamlit as st
from story_engine import StoryEngine


st.set_page_config(
    page_title="Neon Circuit Story Engine",
    page_icon="🏎️",
    layout="centered"
)

import base64

def add_bg_image():
    image_path = os.path.join(os.path.dirname(__file__), "background.png")

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Background */
        .stApp {{
            background: linear-gradient(
                rgba(10,10,15,0.65),
                rgba(10,10,15,0.65)
            ),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Transparent header */
        [data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Main container */
        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        /* Title */
        h1 {{
            color: #00ffff;
            text-shadow: 0 0 10px #00ffff,
                         0 0 20px #00ffff;
            font-family: "Courier New", monospace;
        }}

        /* Subtitle */
        p {{
            color: #e8e8e8;
        }}

        /* Text inputs */
        .stTextInput input {{
            background-color: rgba(15,20,30,0.80);
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 8px;
        }}

        /* Buttons */
        .stButton button {{
            background-color: rgba(15,20,30,0.85);
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 10px;
            box-shadow: 0 0 10px #00ffff;
        }}

        .stButton button:hover {{
            box-shadow: 0 0 20px #00ffff;
            color: white;
        }}

        /* Expanders */
        .streamlit-expanderHeader {{
            color: #00ffff;
        }}

        /* Divider */
        hr {{
            border-color: rgba(0,255,255,0.25);
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

add_bg_image()

# Initialize session state
if "story_history" not in st.session_state:
    st.session_state.story_history = []

if "engine" not in st.session_state:
    st.session_state.engine = StoryEngine()

if "error_message" not in st.session_state:
    st.session_state.error_message = None


# Header
st.title("🏎️ Neon Circuit Story Engine")
st.markdown("*A futuristic city where cars are alive and legends are born on the asphalt.*")
st.divider()


# Input section
col1, col2 = st.columns(2)

with col1:
    character_name = st.text_input(
        "Character Name",
        placeholder="e.g. Shadow V12",
        max_chars=50
    )

with col2:
    car_type = st.text_input(
        "Car Type",
        placeholder="e.g. Stealth Hypercar",
        max_chars=50
    )


# Character counter feedback
if character_name:
    remaining = 50 - len(character_name)
    if remaining < 10:
        st.caption(f"⚠️ {remaining} characters remaining")

# Generate button
generate = st.button(
    "⚡ Generate Story",
    use_container_width=True,
    type="primary"
)

if generate:
    st.session_state.error_message = None

    if not character_name.strip() or not car_type.strip():
        st.session_state.error_message = "Please fill in both fields before generating."
    else:
        with st.spinner("Generating your Neon Circuit story..."):
            try:
                story = st.session_state.engine.generate_story(
                    character_name.strip(),
                    car_type.strip()
                )
                st.session_state.story_history.append({
                    "character": character_name.strip(),
                    "car": car_type.strip(),
                    "story": story
                })

            except ValueError as e:
                st.session_state.error_message = str(e)
            except RuntimeError as e:
                st.session_state.error_message = str(e)

# Error display
if st.session_state.error_message:
    st.error(f"⚠️ {st.session_state.error_message}")

# Latest story display
if st.session_state.story_history:
    latest = st.session_state.story_history[-1]
    st.divider()

    st.markdown(f"### {latest['character']}'s Story")
    st.caption(f"🚗 {latest['car']}")
    st.write(latest["story"])

    # Copy-friendly display
    with st.expander("📋 Copy story text"):
        st.code(latest["story"], language=None)

# Story history
if len(st.session_state.story_history) > 1:
    st.divider()
    st.markdown("### 📖 Story History")

    for entry in reversed(st.session_state.story_history[:-1]):
        with st.expander(f"🏎️ {entry['character']} — {entry['car']}"):
            st.write(entry["story"])

# Clear button
if st.session_state.story_history:
    st.divider()
    if st.button("🗑️ Clear All Stories", use_container_width=True):
        st.session_state.story_history = []
        st.session_state.error_message = None
        st.rerun()

# Footer
st.divider()
st.caption("Neon Circuit Story Engine · Powered by Groq · Part of the Dravon Universe")