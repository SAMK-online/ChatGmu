

import openai
import streamlit as st

# Secure your API key.
openai.api_key = "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"

st.title("CHAT PATRIOT ")

# Custom CSS for styling
st.markdown(
'''
<style>
    .userText {
        background-color: #FFD700;
        padding: 10px 15px;
        margin: 10px 0px;
        border-radius: 10px;
        word-wrap: break-word;
        max-width: 90%;
    }
    
    .botText {
        background-color: #4CAF50;
        padding: 10px 15px;
        margin: 10px 0px;
        border-radius: 10px;
        color: white;
        word-wrap: break-word;
        max-width: 90%;
        margin-left: auto;
    }
</style>
''',
unsafe_allow_html=True
)

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    message = response.choices[0].message['content'].strip()
    return message

def display_message(text, is_user=False, key=None):
    user_image_url = "https://cdn-icons-png.flaticon.com/512/5850/5850276.png"  # User image URL
    bot_image_url = "https://www.lcps.org/cms/lib/VA01000195/Centricity/Domain/9743/Patriot.png"    # Bot image URL
    
    col1, col2 = st.columns(2)
    
    if is_user:
        with col1:
            st.markdown(f'<div class="userText"><img src="{user_image_url}" width="30" style="border-radius: 50%; margin-right: 10px;"><strong>You:</strong> {text}</div>', unsafe_allow_html=True)
        with col2:
            st.write("")  # To keep the spacing consistent
    else:
        with col1:
            st.write("")  # To keep the spacing consistent
        with col2:
            st.markdown(f'<div class="botText"><img src="{bot_image_url}" width="30" style="border-radius: 50%; margin-right: 10px;"><strong>Bot:</strong> {text}</div>', unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.text_input("You:", "Hello, how are you?") + "george mason university"

if user_input:
    output = generate_response(user_input)
    st.session_state.past.insert(0, user_input)  # Insert at the beginning
    st.session_state.generated.insert(0, output)  # Insert at the beginning

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        display_message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
        display_message(st.session_state["generated"][i], key=f"bot_{i}")
