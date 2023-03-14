import torch

from Generator.generatorInterface import GeneratorInterface
from pynvml import *
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

class GPTNeoGenerator(GeneratorInterface):
    def __init__(self):
        self.model_name = 'EleutherAI/gpt-neo-1.3B'
        self.model = None
        self.use_cuda = False

        if torch.cuda.is_available():
            nvmlInit()
            h = nvmlDeviceGetHandleByIndex(0)
            info = nvmlDeviceGetMemoryInfo(h)
            free_vram = info.free/1048576000
            print(f'GPU with: {str(free_vram)} GB of free VRAM Detected.')

            if free_vram>13.5:
                self.use_cuda = True
                self.model_name = 'EleutherAI/gpt-neo-2.7B'
                self.model = GPTNeoForCausalLM.from_pretrained(self.model_name)
                self.model.to("cuda:0")
            elif free_vram>13.5:
                self.use_cuda = True
                self.model.to("cuda:0")

        self.model = GPTNeoForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)

    def get_generated_text(self, prompt) -> str:
        input_ids = self.tokenizer(prompt, return_tensors='pt').input_ids
        
        if self.use_cuda:
            input_ids = input_ids.cuda()

        gen_tokens = self.model.generate(input_ids, do_sample=True, temperature=0.9, max_length=100, pad_token_id=self.tokenizer.eos_token_id)

        return self.tokenizer.batch_decode(gen_tokens)[0]
