
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