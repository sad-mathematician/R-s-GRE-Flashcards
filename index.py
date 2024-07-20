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
    color: #4B4B96;
}
.stButton>button {
    width: 100%;
    background-color: #4B4B96;
    color: white;
    border: none;
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #3A3A7F;
}
.st-info-box {
    background-color: #D9EAD3;
    border-left: 5px solid #4B4B96;
    padding: 10px;
    border-radius: 5px;
    color: #333;
    font-size: 16px;
}
.st-example-box {
    background-color: #FCE5CD;
    border-left: 5px solid #FF9900;
    padding: 10px;
    border-radius: 5px;
    color: #333;
    font-size: 16px;
    margin-top: 10px;
}
.sidebar .sidebar-content {
    background-color: #4B4B96;
    color: white;
}
.sidebar .sidebar-content img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10px;
}
.progress-bar {
    height: 20px;
    background-color: #E0E0E0;
    border-radius: 10px;
    margin-top: 10px;
}
.progress {
    height: 100%;
    background-color: #4B4B96;
    border-radius: 10px;
    transition: width 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('wordlist2.csv', usecols=['word', 'definition', 'example'])
    return data

data = load_data()

# Initialize session state variables
if 'randw' not in st.session_state:
    st.session_state.randw = random.randint(0, len(data) - 1)
if 'show_meaning' not in st.session_state:
    st.session_state.show_meaning = False
if 'seen_words' not in st.session_state:
    st.session_state.seen_words = set()

# Functions
def next_word():
    st.session_state.randw = random.randint(0, len(data) - 1)
    st.session_state.show_meaning = False

def toggle_meaning():
    st.session_state.show_meaning = not st.session_state.show_meaning
    if st.session_state.show_meaning:
        st.session_state.seen_words.add(st.session_state.randw)

# Sidebar
with st.sidebar:
    st.title("GRE Prep Dashboard")
    st.write("Total words:", len(data))
    st.write("Unique words encountered:", len(st.session_state.seen_words))
    
    progress = len(st.session_state.seen_words) / len(data) * 100
    st.write(f"Progress: {progress:.2f}%")
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress" style="width: {progress}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reset Progress"):
        st.session_state.seen_words.clear()
        st.experimental_rerun()

# Main content
colored_header(label="Welcome to Rishabh's GRE Wordlist Prep!", description="Master vocabulary with interactive flashcards", color_name="blue-70")
add_vertical_space(2)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f'<p class="big-font">{data.iloc[st.session_state.randw]["word"]}</p>', unsafe_allow_html=True)
    
    if st.session_state.show_meaning:
        st.markdown(f'<div class="st-info-box">{data.iloc[st.session_state.randw]["definition"]}</div>', unsafe_allow_html=True)
        example = data.iloc[st.session_state.randw]["example"]
        if pd.notna(example):
            st.markdown(f'<div class="st-example-box"><strong>Example:</strong> {example}</div>', unsafe_allow_html=True)
    else:
        st.info("Click 'Reveal Meaning' to see the definition")

with col2:
    st.button("Reveal Meaning" if not st.session_state.show_meaning else "Hide Meaning", on_click=toggle_meaning, key="reveal")
    add_vertical_space(1)
    st.button("Next Word", on_click=next_word)

# Footer
st.markdown("---")
st.write("Created by Rishabh Fuke | 2023")
