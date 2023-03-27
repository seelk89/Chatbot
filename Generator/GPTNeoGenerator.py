import torch
from pynvml import *
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

from Generator.generatorInterface import GeneratorInterface

class GPTNeoGenerator(GeneratorInterface):
    def __init__(self):
        self.model_name = 'EleutherAI/gpt-neo-1.3B'
        self.model = None
        self.use_cuda = False

        # Check if a GPU is available
        if torch.cuda.is_available():
            nvmlInit()
            h = nvmlDeviceGetHandleByIndex(0)
            info = nvmlDeviceGetMemoryInfo(h)
            free_vram = info.free/1048576000
            print(f'GPU with {free_vram:.2f} GB of free VRAM detected.')

            if free_vram > 13.5:
                self.use_cuda = True
                self.model_name = 'EleutherAI/gpt-neo-2.7B'
            elif free_vram > 7:
                self.use_cuda = True

        # Load the model
        self.model = GPTNeoForCausalLM.from_pretrained(self.model_name, cache_dir='./Models')
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name, cache_dir='./Models')

        # Move the model to the GPU if available
        if self.use_cuda:
            self.model.to('cuda:0')

    def get_generated_text(self, prompt) -> str:
        try:
            # Tokenize the input prompt
            input_ids = self.tokenizer(prompt, return_tensors='pt', max_length=1024).input_ids

            # Move the input to the GPU if available
            if self.use_cuda:
                input_ids = input_ids.cuda()

            # Generate text
            gen_tokens = self.model.generate(input_ids, do_sample=True, temperature=0.9, max_length=50, pad_token_id=self.tokenizer.eos_token_id)

            # Decode the generated text
            generated_text = self.tokenizer.batch_decode(gen_tokens)[0].strip()

            return generated_text

        except Exception as e:
            print(f'Error generating text: {str(e)}')
            return ''
