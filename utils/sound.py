from scipy.io.wavfile import write
import speech_recognition as sr
from pydub import AudioSegment
import sounddevice as sd

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

# Convert MP3 to WAV
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    AudioSegment.converter = './/ffmpeg.exe'
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")
