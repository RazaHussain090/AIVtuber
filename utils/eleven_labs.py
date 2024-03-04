import requests
import sound

def synthesize_text_with_elevenlabs(message, api_key=""):
    # Define the URL and request headers
    url = "https://api.elevenlabs.io/v1/text-to-speech/LcfcDJNUP1GQjkzn1xUU/stream"
    headers = {
        "xi-api-key": "",
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
                sound.convert_mp3_to_wav(audio,"output.wav")
                playsound("C:/Users/pc/Documents/GitHub/AIVtuber/output.wav")
                
        else:
            print("Unexpected response content type:", response.headers.get("Content-Type"))
            print("Error "+ response)
    else:
        print("Request failed with status code:", response.status_code)
        print("Error ", response)

