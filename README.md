# Spectre Ai Assistant

This repository contains two Python scripts that implement a voice-assisted conversational AI: `chat.py` and `ui.py`. Both scripts leverage various libraries and Google's Gemini Pro 1.5 to create an engaging and interactive user experience, with `ui.py` extending the functionality to a web interface using Streamlit.

## Features

- **Voice and Text Input:** Allows users to interact via voice or text.
- **Sentiment Analysis:** Analyzes user input for sentiment and responds with appropriate emotional tones.
- **Small Talk Handling:** Provides predefined responses for common small talk queries.
- **Logging:** Logs all interactions and errors for debugging purposes.
- **Web Interface:** `ui.py` provides a Streamlit-based web interface for the assistant.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python 3.7 or higher
- Virtual environment too

### Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/thrive_spectrexq/Spectre_Ai_Assistant.git
    cd Spectre_Ai_Assistant
    ```

2. **Create and Activate a Virtual Environment (Optional):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**
    Create a `.env` file in the root directory and add your Google API key:
    ```sh
    GOOGLE_API_KEY=your_google_api_key
    ```

5. **Download NLTK Data:**
    The required NLTK data will be downloaded automatically when the scripts are run.

### Running the Scripts

#### Running `chat.py`

`chat.py` is a CLI-based interactive assistant. To run the script:
```sh
python chat.py
```

#### Running `ui.py`

`ui.py` provides a web-based interface using Streamlit. To run the script:
```sh
streamlit run ui.py
```

## Script Details

### chat.py

This script integrates voice recognition, text-to-speech, and Google Gemini for generating responses. It features:

- **Text-to-Speech:** Converts text responses to speech.
- **Speech Recognition:** Captures and transcribes user speech input.
- **Small Talk Handling:** Predefined responses for casual conversation.
- **Sentiment Analysis:** Analyzes user sentiment and adjusts responses accordingly.
- **Conversation History:** Maintains the context of the conversation.

### ui.py

`ui.py` extends `chat.py` by adding a web-based interface using Streamlit. It features:

- **Streamlit Interface:** Provides a web UI for the assistant.
- **Session State Management:** Uses Streamlit's session state to maintain conversation history.
- **Voice and Text Input:** Users can choose to interact via typing or speaking.

## Logging

Both scripts are configured to log interactions and errors. Logs are written to the console and can be reviewed for debugging purposes.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License

These scripts are licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Streamlit](https://www.streamlit.io/) for the web-based interface.
- [LangChain](https://langchain.com/) for integration with Google Gemini.
- [Google Gemini](https://deepmind.google/technologies/gemini/pro/) for integration with Google Gemini API

---

