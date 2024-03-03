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
        speak(response_text)

if __name__ == "__main__":
    create_ai_vtuber_chatbot()
