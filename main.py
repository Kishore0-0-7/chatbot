import os

try:
    import google.generativeai as gen_ai
except ImportError:
    import streamlit as st
    st.error("Required package 'google-generativeai' is not installed. Please install it using: pip install google-generativeai")
    st.stop()

import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Direct API key configuration
GOOGLE_API_KEY = "AIzaSyAuB44r81kNaTBZS28WPVn46eNcnd3dUa8"
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found. Please set it in your environment variables or .env file.")
    st.stop()

# Set up Google Gemini-Pro AI model
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')
    # Test the API key with a simple generation
    model.generate_content("Test")
except Exception as e:
    st.error(f"Error initializing Gemini-Pro: {str(e)}")
    st.error("Please check if your API key is valid and properly configured.")
    st.stop()


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    """
    Translate the role from Gemini-Pro terminology to Streamlit terminology.

    Args:
        user_role (str): The role from Gemini-Pro.

    Returns:
        str: The translated role for Streamlit.
    """
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 The Care Crew - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask he Care Crew - ChatBot...")
if user_prompt:
    try:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Error communicating with Gemini-Pro: {str(e)}")
