# model_loader.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from abc import ABC, abstractmethod
from config import DEVICE_INFO

class BaseModelLoader(ABC):
    """
    模型加载器的基类，定义通用接口和方法。
    """

    def __init__(self, model_path, embedding_path, max_new_tokens=512):
        self.model_path = model_path
        self.embedding_path = embedding_path
        self.max_new_tokens = max_new_tokens
        self.tokenizer = None
        self.model = None
        self.llm_pipeline = None
        self.llm = None
        self.embeddings = None

    @abstractmethod
    def load_llm(self):
        """
        抽象方法，由子类实现具体的模型加载逻辑。
        """
        pass

    @abstractmethod
    def load_embeddings(self):
        """
        抽象方法，由子类实现具体的 embedding 加载逻辑。
        """
        pass

    def get_llm(self):
        """
        返回封装好的 LLM，可用于 LangChain。
        """
        if self.llm is None:
            raise ValueError("模型尚未加载，请先调用 load_model() 方法。")
        return self.llm

    def get_embeddings(self):
        """
        返回加载好的 embeddings。
        """
        if self.embeddings is None:
            raise ValueError("Embedding 模型尚未加载，请先调用 load_embeddings() 方法。")
        return self.embeddings

class CUDAModelLoader(BaseModelLoader):
    """
    在 CUDA（GPU）上加载模型和 embedding，支持多卡。
    """

    def __init__(self, model_path, embedding_path, max_new_tokens=512, devices=None):
        super().__init__(model_path, embedding_path, max_new_tokens)
        self.devices = devices

    def load_llm(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype="auto",
            device_map='auto',  # 自动将模型切分到多个 GPU 上
            low_cpu_mem_usage=True
        )
        # 创建 pipeline
        self.llm_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=self.max_new_tokens,
            truncation=True
        )
        self.llm = HuggingFacePipeline(pipeline=self.llm_pipeline)

    def load_embeddings(self):
        # 在 CUDA 设备上加载 embeddings，因为运算量小，通常用单卡，使用多卡通信消耗反而更大
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_path, model_kwargs={'device': 0})

class CPUModelLoader(BaseModelLoader):
    """
    在 CPU 上加载模型和 embedding。
    """

    def load_llm(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            low_cpu_mem_usage=True
        )
        self.llm_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=self.max_new_tokens,
            truncation=True,
            device=-1  # 使用 CPU
        )
        self.llm = HuggingFacePipeline(pipeline=self.llm_pipeline)

    def load_embeddings(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_path)

class MPSModelLoader(BaseModelLoader):
    """
    在 MPS（Apple Silicon）上加载模型和 embedding。
    """

    def load_llm(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            low_cpu_mem_usage=True
        )
        self.model.to('mps')
        self.llm_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=self.max_new_tokens,
            truncation=True,
            device='mps'
        )
        self.llm = HuggingFacePipeline(pipeline=self.llm_pipeline)

    def load_embeddings(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_path, model_kwargs={'device': 'mps'})

def load_model(model_path, embedding_path, max_new_tokens=512):
    """
    根据可用的设备类型，返回相应的 ModelLoader 实例。
    """
    device_type = DEVICE_INFO['device_type']
    devices = DEVICE_INFO['devices']
    
    if device_type == 'cuda':
        return CUDAModelLoader(model_path, embedding_path, max_new_tokens, devices)
    elif device_type == 'mps':
        return MPSModelLoader(model_path, embedding_path, max_new_tokens)
    else:
        return CPUModelLoader(model_path, embedding_path, max_new_tokens)
