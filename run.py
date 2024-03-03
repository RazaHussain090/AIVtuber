import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from transformers import pipeline, Conversation
from gtts import gTTS
from playsound import playsound
import os


def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")  # Clean up the temporary file

def record_audio(duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1,  dtype='int16')
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, recording)  # Save as WAV file 
    print("Recording stopped.")

def speech_to_text(file_path='output.wav'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized text:", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ""

from pydub import AudioSegment

# Convert MP3 to WAV
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    AudioSegment.converter = 'ffmpeg.exe'
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")

import requests
import json

def synthesize_text_with_voicevox(text, speaker=1):
    url = "http://localhost:50021/audio_query"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"text": text, "speaker": speaker})
    
    # Step 1: Generate Audio Query
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print("Failed to generate audio query")
        return

    audio_query = response.json()

    # Step 2: Synthesize Audio
    synthesis_url = "http://localhost:50021/synthesis"
    synthesis_response = requests.post(synthesis_url, headers=headers, data=json.dumps(audio_query), params={"speaker": speaker})
    if synthesis_response.status_code != 200:
        print("Failed to synthesize audio")
        return

    # Step 3: Save or Play the Audio
    with open("output.wav", "wb") as audio_file:
        audio_file.write(synthesis_response.content)
    print("Audio synthesized and saved as output.wav.")

def synthesize_text_with_elevenlabs(message, api_key=""):
    # Define the URL and request headers
    url = "https://api.elevenlabs.io/v1/text-to-speech/LcfcDJNUP1GQjkzn1xUU/stream"
    headers = {
        "xi-api-key": "replace with your api key",
        "Content-Type": "application/json"
    }

    # Define the request payload (JSON data)
    payload = {
        "text": message,
        "model_id": "eleven_multilingual_v1"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code and content
    if response.status_code == 200:
        # If the response content type is audio/mpeg, you can save it to a file
        if response.headers.get("Content-Type") == "audio/mpeg":
            with open("audio.mp3", "wb") as audio_file:
                audio_file.write(response.content)
                print("mp3 done")
                audio = "audio.mp3"
                convert_mp3_to_wav(audio,"output.wav")
                playsound("C:/Users/pc/Documents/GitHub/AIVtuber/output.wav")
                
        else:
            print("Unexpected response content type:", response.headers.get("Content-Type"))
            print("Error "+ response)
    else:
        print("Request failed with status code:", response.status_code)
        print("Error ", response)



def create_ai_vtuber_chatbot():
    chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium", return_dict=False )
    print("AI VTuber Chatbot initialized. Speak 'quit' to exit.")

    while True:
        record_audio(duration=5)  # Record for 5 seconds
        user_input = speech_to_text()
        print(f"You said: {user_input}")
        if user_input.lower() == 'quit':
            break
        
        conversation = Conversation(user_input)
        response = chatbot(conversation)
        print("AI VTuber:", response.generated_responses[0])
        response_text = response.generated_responses[0]
        # Convert the chatbot's response to speech
        synthesize_text_with_elevenlabs(response_text)

if __name__ == "__main__":
    create_ai_vtuber_chatbot()
    # Example usage
    #text_to_speak = "こんにちは、VOICEVOXです。"
    #synthesize_text_with_voicevox(text_to_speak)
    # Example usage

