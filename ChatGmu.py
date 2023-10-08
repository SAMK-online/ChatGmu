import openai
import requests
import streamlit as st
import http.client
import json
from bs4 import BeautifulSoup

# Secure your API key.
openai.api_key = "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"

st.title("CHAT PATRIOT" + ":robot_face:")

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

bg_image = "https://patriothacks.org/wp-content/uploads/2023/09/pixel-guy.png"

# Custom CSS to set the background
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url({bg_image});
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_google_serper_results(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def extract_relevant_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(['script', 'style', 'footer', 'header', 'nav']):
        script.extract()
    text = soup.get_text()
    return ' '.join(text.split())[:1000] 

def extract_relevant_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for script in soup(['script', 'style', 'footer', 'header', 'nav']):
        script.extract()
    
    # Extract text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing spaces
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def fetch_content_from_links(search_results):
    # Increase the number of links to fetch from (e.g., top 5 links)
    links = search_results.get('links', [])[:5]
    
    # Blocklist of domains that are known to be non-relevant or broken
    blocklist = ['example.com', 'another-example.com']

    content_list = []
    for link in links:
        # Skip links from the blocklist
        if any(blocked_domain in link for blocked_domain in blocklist):
            continue
        
        try:
            response = requests.get(link, timeout=5)
            response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes
            content = extract_relevant_content_from_html(response.text)
            content_list.append(content)
            
            # Optionally limit to the first 3 successful content extractions
            if len(content_list) >= 3:
                break
        except requests.RequestException:
            # This will catch any issues with the request, including timeouts
            continue

    combined_content = "\n\n".join(content_list)
    return combined_content



def generate_response(prompt):
    # Fetch search results
    search_results = fetch_google_serper_results(prompt)
    links = search_results.get('links', [])[:3]  # Get top 3 links
    
    # Return the top relevant links to the user
    link_message = "Relevant links based on your query:\n"
    link_message += '\n'.join(links)
    
    # Fetch content from those links
    content = fetch_content_from_links(search_results)
    
    combined_prompt = f"My Query '{prompt}':\n\nWeb context: \n{content}\n\nUse this context to give summarizing answer. Include all links in your answer as well"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_prompt}
        ]
    )
    chatbot_message = response.choices[0].message['content'].strip()
    
    # Combine the link message, extracted content, and the chatbot's response
    final_response = f"{link_message}\n\n\n{content}\n\n\n{chatbot_message}"
    
    return final_response




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

user_input = st.text_input("")
user_search_query = user_input + "George Mason University"

if user_input:
    output = generate_response(user_search_query)
    st.session_state.past.insert(0, user_input)  # Insert at the beginning
    st.session_state.generated.insert(0, output)  # Insert at the beginning

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        display_message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
        display_message(st.session_state["generated"][i], key=f"bot_{i}")
