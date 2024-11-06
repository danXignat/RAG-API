from llama_index.llms.ollama import Ollama
from config.settings import LLM_MODEL_NAME

llm = Ollama(LLM_MODEL_NAME, request_timeout=120)

response = llm.stream_complete("tell me a long long story")

for r in response:
    print(r.delta, end='', flush=True)