import os
import pyttsx3
import pyaudio
import speech_recognition as sr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from textblob import TextBlob  # For basic sentiment analysis
import nltk
import random
import logging
import streamlit as st
from langchain.globals import set_verbose, get_verbose

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Check and download necessary NLTK corpora for textblob if not already present
nltk_data_path = os.path.expanduser("~/nltk_data")
if not os.path.exists(nltk_data_path):
    os.mkdir(nltk_data_path)

nltk.data.path.append(nltk_data_path)


def download_corpora():
    corpora = ["brown", "punkt"]
    for corpus in corpora:
        try:
            nltk.data.find(f"corpora/{corpus}")
        except LookupError:
            nltk.download(corpus, download_dir=nltk_data_path)


download_corpora()

# 1. Load API Key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Set Up Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=api_key)

# 3. Set up Text-to-Speech (TTS)
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Use the default voice

# 4. Set up Speech Recognition
r = sr.Recognizer()
mic = sr.Microphone()

# Initialize Streamlit session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen for voice input and return the transcribed text."""
    with mic as source:
        logging.info("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        logging.error("Could not understand the audio.")
        st.error("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition; {e}")
        st.error(f"Could not request results from Google Speech Recognition; {e}")
        return None


def get_response(prompt):
    """Get response from the LLM."""
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    messages = [
        {"role": "system", "content": "You are a helpful and friendly assistant."}
    ] + st.session_state.conversation_history
    response = llm.invoke(prompt).content
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": response}
    )
    return response


def handle_small_talk(prompt):
    """Handle small talk or casual conversation."""
    small_talk_responses = {
        "how are you": "I'm just a computer program, but I'm doing great! How about you?",
        "what's your name": "I'm your friendly assistant. You can call me whatever you like.",
        "what's the weather": "I don't have weather data right now, but you can check your local weather app!",
        # Add more small talk responses as needed
    }
    for key in small_talk_responses:
        if key in prompt.lower():
            return small_talk_responses[key]
    return None


def analyze_emotion(text):
    """Analyze the emotion of the text and return an appropriate response."""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.2:
        return "happy"
    elif analysis.sentiment.polarity < -0.2:
        return "sad"
    else:
        return "neutral"


def expressive_speak(text, emotion):
    """Speak the text with an expressive tone."""
    if emotion == "happy":
        engine.say(text + " Ha ha ha!")
    elif emotion == "sad":
        engine.say(text + " I'm here for you.")
    else:
        engine.say(text)
    engine.runAndWait()


# Streamlit UI
st.title("Spectre's Assistant")

# Welcome message
if "welcome_message" not in st.session_state:
    welcome_messages = [
        "Welcome Spectre, how may I assist you today, Sir?",
        "Hello Spectre! What can I do for you today?",
        "Hi Spectre! How can I help you today?",
    ]
    st.session_state.welcome_message = random.choice(welcome_messages)
    st.write(st.session_state.welcome_message)
    speak(st.session_state.welcome_message)

input_mode_message = "Would you like to type your prompt or speak to me?"
st.write(input_mode_message)

# UI for user to choose input method
input_method = st.radio("Choose your input method:", ("Type", "Speak"))

if input_method == "Type":
    prompt = st.text_input("You:")
    if st.button("Submit"):
        if prompt:
            small_talk_response = handle_small_talk(prompt)
            if small_talk_response:
                response = small_talk_response
            else:
                response = get_response(prompt)

            emotion = analyze_emotion(prompt)
            logging.info(
                f"User prompt: {prompt} | AI response: {response} | Emotion: {emotion}"
            )
            st.write(f"AI ({emotion}): {response}")
            expressive_speak(response, emotion)
elif input_method == "Speak":
    st.write("Click 'Listen' and start speaking.")
    if st.button("Listen"):
        prompt = listen()
        if prompt:
            st.write(f"You: {prompt}")
            small_talk_response = handle_small_talk(prompt)
            if small_talk_response:
                response = small_talk_response
            else:
                response = get_response(prompt)

            emotion = analyze_emotion(prompt)
            logging.info(
                f"User prompt: {prompt} | AI response: {response} | Emotion: {emotion}"
            )
            st.write(f"AI ({emotion}): {response}")
            expressive_speak(response, emotion)

# UI for another question
if st.button("Do you have another question?"):
    st.experimental_rerun()
