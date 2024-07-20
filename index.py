import streamlit as st
import random
import pandas as pd
# streamlit run /Users/rishabhfuke/Desktop/Programming/flashcards_app/main.py
st.title('Welcome to Rishabh GRE wordlist prep!')
data = pd.read_csv('wordlist2.csv')

# to ensure random value of var doesn't change on its own
if 'randw' not in st.session_state:
    st.session_state.randw = random.randint(1, 324)

# accessing the specific word
word = data.iloc[st.session_state.randw]['word']
meaning = data.iloc[st.session_state.randw]['definition']

st.write(word)

# buttons
# count = 0
seemeaning_msg = 'See what this means'

def NextWord():
    st.session_state.randw = random.randint(1, 324)
    st.experimental_rerun()  # Rerun the script to update the displayed word

# if count == 1:
#     seemeaning_msg = 'Next word'
    
seemeaning = st.button(seemeaning_msg)

if seemeaning:
    st.write(meaning)
    # count += 1
    # print(count)


# if count == 2:
#     NextWord()

if st.button('Next word'):
    NextWord()
