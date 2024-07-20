import streamlit as st
import random
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# Set page config
st.set_page_config(page_title="GRE Wordlist Prep", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('wordlist2.csv', usecols=['word', 'definition', 'example'])
    return data.dropna()

data = load_data()

# Initialize session state variables
if 'randw' not in st.session_state:
    st.session_state.randw = random.randint(0, len(data) - 1)
if 'show_meaning' not in st.session_state:
    st.session_state.show_meaning = False

# Functions
def next_word():
    st.session_state.randw = random.randint(0, len(data) - 1)
    st.session_state.show_meaning = False

def toggle_meaning():
    st.session_state.show_meaning = not st.session_state.show_meaning

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Educational_Testing_Service_logo.svg/220px-Educational_Testing_Service_logo.svg.png", width=200)
    st.title("GRE Prep Dashboard")
    st.write("Total words:", len(data))
    if st.button("Reset Progress"):
        st.session_state.clear()
        st.experimental_rerun()

# Main content
colored_header(label="Welcome to Rishabh's GRE Wordlist Prep!", description="Master vocabulary with interactive flashcards", color_name="blue-70")

add_vertical_space(2)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f'<p class="big-font">{data.iloc[st.session_state.randw]["word"]}</p>', unsafe_allow_html=True)
    
    if st.session_state.show_meaning:
        st.info(data.iloc[st.session_state.randw]["definition"])
        example = data.iloc[st.session_state.randw]["example"]
        if pd.notna(example):
            st.markdown(f"**Example:** {example}")
    else:
        st.info("Click 'Reveal Meaning' to see the definition")

with col2:
    st.button("Reveal Meaning" if not st.session_state.show_meaning else "Hide Meaning", on_click=toggle_meaning, key="reveal")
    add_vertical_space(1)
    st.button("Next Word", on_click=next_word)

# Progress tracking (placeholder for future feature)
add_vertical_space(2)
st.progress(0.5, text="Progress Placeholder")

# Footer
st.markdown("---")
st.write("Created by Rishabh Fuke | 2023")
