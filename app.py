import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Your Cool Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 Cool Chatbot")
    st.markdown("This is a simple rule-based chatbot created with Streamlit.")
    st.markdown("Feel free to chat and ask it questions!")
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "This chatbot uses basic Python logic to respond to your messages. "
        "It's a great starting point for building more complex conversational AI."
    )

# --- Chatbot Logic ---
def get_bot_response(user_input):
    """
    Generates a response from the bot based on user input.
    """
    user_input = user_input.lower()
    greetings = ["hello", "hi", "hey", "hola"]
    farewells = ["bye", "goodbye", "see you"]
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An Impasta!",
    ]

    if any(word in user_input for word in greetings):
        return "Hello there! How can I assist you today?"
    elif any(word in user_input for word in farewells):
        return "Goodbye! Have a great day!"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! Thanks for asking."
    elif "your name" in user_input:
        return "You can call me the Cool Chatbot. What's your name?"
    elif "joke" in user_input:
        return random.choice(jokes)
    elif "time" in user_input:
        return f"The current time is {time.strftime('%H:%M:%S')}."
    elif "help" in user_input:
        return "You can ask me for a joke, the time, or just chat with me. Try asking 'tell me a joke'."
    else:
        return "I'm not sure how to respond to that. Try asking for help."


# --- Main Application ---

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        with st.spinner("Thinking..."):
            time.sleep(0.5)  # Simulate thinking time
            assistant_response = get_bot_response(prompt)
        # Simulate typing effect
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
