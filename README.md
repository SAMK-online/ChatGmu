# ChatGmu
Chat GMU is an AI chatbot built using openAI api and streamlit, hosted on the Amazon EC2 servers. The project is essentially a web-based chatbot interface where a user can input a query. Instead of directly querying the GPT-3 model, the system first searches the web for relevant information using the Google Serper API. It then processes the top results, extracting relevant text content. This content is then passed to the GPT-3 model, which generates a response based on the fetched information.

This approach is particularly useful when the user's query requires up-to-date or factual information from the web, which GPT-3 might not have in its training data. The system essentially augments GPT-3's capabilities with real-time web search results.

link to access the chatbot: http://18.219.46.204:8501/

<img width="1440" alt="Screenshot 2023-10-08 at 10 12 59 AM" src="https://github.com/SAMK-online/ChatGmu/assets/71158786/0077c396-f604-4a7a-ae4f-bca381c5ae26">
<img width="1223" alt="Screenshot 2023-10-08 at 10 14 27 AM" src="https://github.com/SAMK-online/ChatGmu/assets/71158786/03e5bd4d-13bf-4c1d-b2e5-3d43240efefc">

