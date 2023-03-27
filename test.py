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

# import threading
# import queue
# import speech_recognition as sr

# def listen_continuous(q):
#     r = sr.Recognizer()
#     mic = sr.Microphone()

#     with mic as source:
#         r.adjust_for_ambient_noise(source)

#     while True:
#         with mic as source:
#             audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             q.put(text)
#         except sr.UnknownValueError:
#             pass

# q = queue.Queue()
# t = threading.Thread(target=listen_continuous, args=(q,))
# t.start()
# while True:
#     text = q.get()
#     print(text)

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
