import os
import pyttsx3
import pyaudio
import speech_recognition as sr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Set Up Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=api_key)

# Set up Text-to-Speech (TTS)
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Use the default voice

# Set up Speech Recognition
r = sr.Recognizer()
mic = sr.Microphone()


# Conversation Loop
def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen for voice input and return the transcribed text."""
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition; {e}")
        return None


# Main Loop
while True:
    print("Choose input method:")
    print("1. Type")
    print("2. Speak")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        prompt = input("You: ")
    elif choice == "2":
        prompt = listen()
        if prompt is None:
            continue  # Skip if speech recognition fails
    else:
        print("Invalid choice.")
        continue

    # Process the prompt and generate a response
    response = llm.invoke(prompt).content
    print(f"AI: {response}")
    speak(response)
