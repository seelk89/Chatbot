import json
import openai
import requests
import keyboard
import threading
import speech_recognition as sr

# File for testing of misc. stuff.

def get_generated_text(prompt) -> str:
        with open('env.json', 'r') as f:
            data = json.load(f)

        # Set up the OpenAI API client
        openai.api_key = data['OPENAI_API_KEY']
        model_engine = 'gpt-3.5-turbo'

        # Send the prompt to the API and receive a response
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=100,
        )

        return response.choices[0].text.strip()

#print(get_generated_text('Who are you?'))

def get_models_to_json():
    with open('env.json', 'r') as f:
        data = json.load(f)

    r = requests.get('https://api.openai.com/v1/models', auth=(data['USER'], data['OPENAI_API_KEY']))

    with open('models.json', 'w') as outfile:
        outfile.write(json.dumps(r.json()))

#get_models_to_json()

def get_model_names_from_json():
    with open('models.json', 'r') as f:
            models = json.load(f)

    for i in models['data']:
        print(i['id'])

#get_model_names_from_json()

# Create a recognizer object
r = sr.Recognizer()

# Define a function to handle the speech recognition
def handle_speech():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)

# Define a function to continuously listen for the key press in a separate thread
def listen_for_key():
    while True:
        if keyboard.is_pressed('ctrl'):
            handle_speech()
        elif keyboard.is_pressed('alt'):
            break
        else:
            print('not test')

# Start the separate thread for listening to the key press
# key_thread = threading.Thread(target=listen_for_key)
# key_thread.start()

#listen_for_key()
