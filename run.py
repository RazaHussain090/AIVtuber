from transformers import pipeline, Conversation
from utils.eleven_labs import *
from utils.sound import *
from utils.tts import *

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