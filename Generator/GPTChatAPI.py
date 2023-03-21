import json
import openai
import requests

from Generator.generatorInterface import GeneratorInterface

# Classes in here are affected by the trafic on OpenAI's api

class OpenaiApiDavinci(GeneratorInterface):
    def get_generated_text(self, prompt) -> str:
        with open('env.json', 'r') as f:
            data = json.load(f)

        # Set up the OpenAI API client
        openai.api_key = data['OPENAI_API_KEY']
        model_engine = 'davinci'

        # Send the prompt to the API and receive a response
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=100,
        )

        return response.choices[0].text.strip()

class OpenaiApiGPT3Turbo(GeneratorInterface):
    def get_generated_text(self, prompt) -> str:
        with open('env.json', 'r') as f:
            data = json.load(f)

        url = 'https://api.openai.com/v1/chat/completions'

        key = data['OPENAI_API_KEY']
        # Set the API authorization token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}'
        }

        # Set the request payload data
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': f'{prompt}'}],
            'temperature': 0.7 # Value between 0 and 2, lower values mean more random responses
        }

        # Send the API request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check if the API request was successful
        if response.status_code == 200:
            # Print the response content (the generated text)

            response_data = json.loads(response.content)

            # According to the docs the api can return multiple choices, this is a way to handle that before the return
            choices = []
            for choice in response_data['choices']:
                choices.append(choice['message']['content'])
            
            string_from_list = "\n\n".join(choices)

            return string_from_list
        else:
            # Print the error message
            return f'Error: {response.status_code}, {response.reason}'
