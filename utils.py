import os
from dotenv import load_dotenv
import base64
import streamlit as st
import openai  # <-- Add this import

# Load the environment variables from the .env file
load_dotenv()
api_key = os.getenv("openai_api_key")

# Initialize the OpenAI client
openai.api_key = api_key  # <-- Initialize the API key directly

def get_answer(message):
    system_message = [{"role": "system", "content": "You are a helpful chatbot that answers questions asked by users."}]
    messages = system_message + [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )
        return transcript['text']

def text_to_speech(input_text):
    response = openai.Audio.create(
        model="text-to-speech",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        f.write(response['audio_content'])
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


