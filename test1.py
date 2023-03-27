from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

from pynvml import *
import torch

tokenizer = LlamaTokenizer.from_pretrained("chavinlo/alpaca-native", cache_dir='D:\\Code\\Ai')

base_model = LlamaForCausalLM.from_pretrained("chavinlo/alpaca-native", cache_dir='D:\\Code\\Ai', low_cpu_mem_usage=True, from_tf=True)

# Check if a GPU is available
if torch.cuda.is_available():
    nvmlInit()
    h = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(h)
    free_vram = info.free/1048576000
    print(f'GPU with {free_vram:.2f} GB of free VRAM detected.')

base_model.to('cuda:0')

pipe = pipeline(
    "text-generation",
    model=base_model, 
    tokenizer=tokenizer, 
    max_length=256,
    temperature=0.6,
    top_p=0.95,
    repetition_penalty=1.2
)

local_llm = HuggingFacePipeline(pipeline=pipe)

from langchain import PromptTemplate, LLMChain

template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: 
{instruction}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["instruction"])

llm_chain = LLMChain(prompt=prompt, 
                     llm=local_llm
                     )

question = "What is the capital of England?"

print(llm_chain.run(question))

question = "What are alpacas? and how are they different from llamas?"

print(llm_chain.run(question))

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# We are going to set the memory to go back 4 turns
window_memory = ConversationBufferWindowMemory(k=4)

conversation = ConversationChain(
    llm=local_llm, 
    verbose=True, 
    memory=window_memory
)

conversation.prompt.template

conversation.prompt.template = '''The following is a friendly conversation between a human and an AI called Alpaca. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. 

Current conversation:
{history}
Human: {input}
AI:'''

conversation.predict(input="What is your name?")

# conversation.predict(input="Can you tell me what an Alpaca is?")

# conversation.predict(input="How is it different from a Llama?")

# conversation.predict(input="Can you give me some good names for a pet llama?")

# conversation.predict(input="Is your name Fred?")

# conversation.predict(input="What food should I feed my new llama?")
