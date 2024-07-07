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

# 5. Conversation Functions
conversation_history = []


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
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition; {e}")
        print(f"Could not request results from Google Speech Recognition; {e}")
        return None


def get_response(prompt):
    """Get response from the LLM."""
    conversation_history.append({"role": "user", "content": prompt})
    messages = [
        {"role": "system", "content": "You are a helpful and friendly assistant."}
    ] + conversation_history
    response = llm.invoke(prompt).content
    conversation_history.append({"role": "assistant", "content": response})
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


# Welcome message
welcome_messages = [
    "Welcome Spectre, how may I assist you today, Sir?",
    "Hello Spectre! What can I do for you today?",
    "Hi Spectre! How can I help you today?",
]
welcome_message = random.choice(welcome_messages)
print(welcome_message)
speak(welcome_message)

# Conversation loop
while True:
    try:
        input_mode_message = "Would you like to type your prompt or speak to me? Say 'yes' to speak, 'no' to type."
        print(input_mode_message)
        speak(input_mode_message)

        choice = listen()
        if choice is None:
            choice = input("Enter your choice (yes/no): ")

        if choice.lower() in ["yes", "y"]:
            speak("Alright Spectre, I am listening to you.")
            prompt = listen()
            if prompt is None:
                continue
        elif choice.lower() in ["no", "n"]:
            prompt = input("You: ")
        else:
            print("Invalid choice. Please say 'yes' or 'no'.")
            continue

        small_talk_response = handle_small_talk(prompt)
        if small_talk_response:
            response = small_talk_response
        else:
            response = get_response(prompt)

        emotion = analyze_emotion(prompt)
        logging.info(
            f"User prompt: {prompt} | AI response: {response} | Emotion: {emotion}"
        )
        print(f"AI ({emotion}): {response}")
        expressive_speak(response, emotion)

        while True:
            another_question_message = (
                "Do you have another question? Say 'yes' or 'no'."
            )
            print(another_question_message)
            speak(another_question_message)

            another_choice = listen()
            if another_choice is None:
                another_choice = input("Enter your choice (yes/no): ")

            if another_choice.lower() in ["yes", "y"]:
                break
            elif another_choice.lower() in [
                "no",
                "n",
                "bye",
                "that will be all for today, thank you",
            ]:
                goodbye_messages = [
                    "Have a nice day, Spectre!",
                    "Goodbye Spectre! Take care!",
                    "See you later, Spectre!",
                ]
                goodbye_message = random.choice(goodbye_messages)
                logging.info("Session ended by user.")
                print(goodbye_message)
                speak(goodbye_message)
                exit()
            else:
                print("Invalid choice. Please say 'yes' or 'no'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        speak("An error occurred. Please try again.")