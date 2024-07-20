import streamlit as st
import random
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_card import card

# Set page config
st.set_page_config(page_title="GRE Wordlist Prep", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    .big-font {
        font-size: 48px !important;
        font-weight: bold;
        color: #4B4B96;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #4B4B96;
        color: white;
        border: none;
        padding: 15px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .stButton>button:hover {
        background-color: #3A3A7F;
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    
    .st-info-box {
        background-color: #E8F0FE;
        border-left: 5px solid #4285F4;
        padding: 20px;
        border-radius: 10px;
        color: #333;
        font-size: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .st-example-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 20px;
        border-radius: 10px;
        color: #333;
        font-size: 18px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .sidebar .sidebar-content {
        background-color: #F0F2F6;
        color: #333;
        padding: 20px;
    }
    
    .sidebar .sidebar-content img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px;
        border-radius: 10px;
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
colored_header(label="GRE Wordlist Prep", description="Master vocabulary with interactive flashcards", color_name="blue-70")
add_vertical_space(2)

st.markdown(f'<p class="big-font">{data.iloc[st.session_state.randw]["word"]}</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.session_state.show_meaning:
        st.markdown(f'<div class="st-info-box">{data.iloc[st.session_state.randw]["definition"]}</div>', unsafe_allow_html=True)
        example = data.iloc[st.session_state.randw]["example"]
        if pd.notna(example):
            st.markdown(f'<div class="st-example-box"><strong>Example:</strong> {example}</div>', unsafe_allow_html=True)
    else:
        card(
            title="Reveal Meaning",
            text="Click the button below to see the definition and example.",
            image="https://images.unsplash.com/photo-1546514714-df0ccc50d7bf?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=80",
        )

col1, col2 = st.columns(2)
with col1:
    st.button("Reveal Meaning" if not st.session_state.show_meaning else "Hide Meaning", on_click=toggle_meaning, key="reveal")
with col2:
    st.button("Next Word", on_click=next_word)

# Footer
st.markdown("---")
st.write("Created by Rishabh Fuke | 2023")
