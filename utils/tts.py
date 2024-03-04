from gtts import gTTS


def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")  # Clean up the temporary file
