import os
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI

# v < 0.60.0
@staticmethod
class LLMS:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4oMini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.8)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.8)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.8)
        # self.Phi3 = Ollama(model="phi3:mini")
        self.Llama3_1 = Ollama(model="llama3.1")
        self.Phi3 = Ollama(model="phi3:medium-128k")
        # self.Phi3 = ChatOpenAI(model_name="phi3:medium-128k", temperature=0, api_key="ollama", base_url="http://localhost:11434")
        # self.groqLama3_8B_3192 = ChatGroq(temperature=0.5, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="llama3-8b-8192")

# v >= 0.60.0
@staticmethod
class LLMS60:
    def __init__(self):
        self.GTP4='gtp-4'
        self.GTP4o='gpt-4o'
        self.GTP4oMini = 'gpt-4o-mini'
        # self.groqLama3_8B_3192 = ChatGroq(temperature=0.5, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="llama3-8b-8192")
        # Ollama
        self.codellama_code = 'ollama/codellama:code'
        self.codellama_instruct = 'ollama/codellama:instruct'
        self.codellama_python = 'ollama/codellama:python'
        self.codellama_latest = 'ollama/codellama:latest'
        self.codegemma_latest = 'ollama/codegemma:latest'
        self.deepseek_coder_v2_latest = 'ollama/deepseek-coder-v2:latest'
        self.gemma2_latest = 'ollama/gemma2:latest'
        self.mistral_latest = 'ollama/mistral:latest'
        self.dolphin_mistral_latest = 'ollama/dolphin-mistral:latest'
        self.mistral_nemo_latest = 'ollama/mistral-nemo:latest'
        self.llama3_1_70= 'ollama/llama3.1:70b'
        self.llama3_1_latest = 'ollama/llama3.1:latest'
        self.phi3_5_latest = 'ollama/phi3.5:latest'
        self.phi3_instruct = 'ollama/phi3:instruct'
        self.phi3_mini = 'ollama/phi3:mini'
        self.phi3_medium_128 = 'ollama/phi3:medium-128k'
        self.phi3_latest = 'ollama/phi3:latest'
        self.phi3_14 = 'ollama/phi3:14b'
