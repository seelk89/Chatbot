import json
import openai

from Generator.generatorInterface import GeneratorInterface

class OpenaiApi(GeneratorInterface):
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
