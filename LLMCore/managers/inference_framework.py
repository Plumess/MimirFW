from abc import ABC, abstractmethod
import os

# ==============================
# 通用 API 推理接口基类
# ==============================
class InferenceFramework(ABC):
    @abstractmethod
    def load_llm(self, llm_model_source, **kwargs):
        """加载 LLM 模型"""
        pass

    @abstractmethod
    def load_embeddings(self, embeddings_model_source, **kwargs):
        """加载 Embedding 模型"""
        pass

    @abstractmethod
    def get_llm(self):
        """返回与 LangChain 兼容的 LLM 对象"""
        pass

    @abstractmethod
    def get_embeddings(self):
        """返回与 LangChain 兼容的 Embedding 模型对象"""
        pass


# ==============================
# OpenAI API 推理接口
# ==============================
class OpenAIAPIFramework(InferenceFramework):
    def __init__(self):
        """
        初始化 API 推理接口。
        """
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, llm_model_source, **llm_kwargs):
        """
        加载 LLM 模型，可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_openai import ChatOpenAI

        self.llm_api_key = llm_kwargs.pop('api_key', os.getenv('OPENAI_API_KEY'))
        if not self.llm_api_key:
            raise ValueError("LLM API 密钥未设置")

        # 如果需要，可以覆盖 base_url
        self.llm_base_url = llm_kwargs.pop('base_url', None)

        self.llm_model = ChatOpenAI(
            model=llm_model_source,
            api_key=self.llm_api_key,
            base_url=self.llm_base_url,
            **llm_kwargs
        )

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        """
        加载 Embeddings 模型，可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_openai import OpenAIEmbeddings

        self.embeddings_api_key = embeddings_kwargs.pop('api_key', os.getenv('OPENAI_API_KEY'))
        if not self.embeddings_api_key:
            raise ValueError("Embeddings API 密钥未设置")

        # 如果需要，可以覆盖 base_url
        self.embedding_base_url = embeddings_kwargs.pop('base_url', None)

        self.embedding_model = OpenAIEmbeddings(
            model=embeddings_model_source,
            api_key=self.embeddings_api_key,
            base_url=self.embedding_base_url,
            **embeddings_kwargs
        )

    def get_llm(self):
        return self.llm_model

    def get_embeddings(self):
        return self.embedding_model


# ==============================
# 阿里云 Qwen2 API 推理接口
# ==============================
class QwenAPIFramework(InferenceFramework):
    def __init__(self):
        """
        初始化 API 推理接口。
        """
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, llm_model_source, **llm_kwargs):
        """
        加载 LLM 模型，可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_community.chat_models.tongyi import ChatTongyi

        self.llm_api_key = llm_kwargs.pop('api_key', os.getenv('DASHSCOPE_API_KEY'))
        if not self.llm_api_key:
            raise ValueError("LLM API 密钥未设置")

        self.llm_model = ChatTongyi(
            model=llm_model_source,
            api_key=self.llm_api_key,
            **llm_kwargs
        )

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        """
        加载 Embeddings 模型，可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_community.embeddings.dashscope import DashScopeEmbeddings

        self.embeddings_api_key = embeddings_kwargs.pop('api_key', os.getenv('DASHSCOPE_API_KEY'))
        if not self.embeddings_api_key:
            raise ValueError("Embeddings API 密钥未设置")
            
        self.embedding_model = DashScopeEmbeddings(
            model=embeddings_model_source,
            **embeddings_kwargs
        )

    def get_llm(self):
        return self.llm_model

    def get_embeddings(self):
        return self.embedding_model


# ==============================
# VLLM 推理接口 
# ==============================
class VLLMFramework(InferenceFramework):
    def __init__(self, devices):
        """
        初始化 VLLM 推理接口。

        devices: 设备列表，例如 ['cuda:0', 'cuda:1', ...]
        """
        self.devices = devices
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, llm_model_source, **llm_kwargs):
        """
        使用 LangChain VLLM 集成接口加载 LLM 模型
        """
        from langchain_community.llms import VLLM

        # 获取可用 GPU 数量
        tensor_parallel_size = len(self.devices)

        self.llm_model = VLLM(
            model=llm_model_source,
            tensor_parallel_size=tensor_parallel_size,
            trust_remote_code=True,  # 适用于需要信任远程代码的 Hugging Face 模型
            **llm_kwargs
        )

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        """
        暂时使用 huggingface 接口加载 Embeddings 模型。

        参数：
        - model_source: 模型路径或名称。
        - kwargs: 其他可选参数，用于传递给 HuggingFaceEmbeddings 方法。
        """

        from langchain_huggingface import HuggingFaceEmbeddings

        if 'cuda' in self.devices[0]:
            embedding_device = 0  # 默认使用第一个 GPU 设备
        elif self.devices == 'cpu':
            embedding_device = 'cpu'
        elif self.devices == 'mps':
            embedding_device = 'mps'
        else:
            embedding_device = 'cpu'  # 默认使用 CPU

        # 创建 Embedding 模型
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embeddings_model_source,
            model_kwargs={'device': embedding_device},
            **embeddings_kwargs
        )

    def get_llm(self):
        if self.llm_model is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm_model

    def get_embeddings(self):
        if self.embedding_model is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.embedding_model

    
# ==============================
# Huggingface Transformers 推理接口（通用，CPU/MPS 未测试）
# ==============================
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class TransformersFramework(InferenceFramework):
    def __init__(self, devices):
        """
        初始化 Transformers 推理接口。

        参数：
        - device: 设备名称，如 'cpu'、'cuda'、'cuda:0'、'mps' 等。
        """
        self.devices = devices
        self.llm_model = None
        self.embedding_model = None
        self.tokenizer = None
        self.model = None

    def set_tokenizer(self, model_source, **tokenizer_kwargs):
        """
        设置 tokenizer。

        参数：
        - model_source: 模型路径或名称。
        - tokenizer_kwargs: 传递给 AutoTokenizer 的参数。
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_source, **tokenizer_kwargs)

    def set_model(self, model_source, **model_kwargs):
        """
        设置模型。

        参数：
        - model_source: 模型路径或名称。
        - model_kwargs: 传递给 AutoModelForCausalLM 的参数，例如：
            - torch_dtype="auto",
            - device_map='auto',  # 自动将模型切分到多个 GPU 上
            - low_cpu_mem_usage=True
        """
        self.model = AutoModelForCausalLM.from_pretrained(model_source, **model_kwargs)

    def set_pipeline(self, **pipeline_kwargs):
        """
        设置 pipeline。

        参数：
        - pipeline_kwargs: 传递给 transformers.pipeline 的参数，例如：
            - max_new_tokens=512,
            - truncation=True
        """
        if not self.tokenizer or not self.model:
            raise ValueError("请先设置 tokenizer 和 model")

        generation_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            **pipeline_kwargs
        )

        self.llm_model = HuggingFacePipeline(pipeline=generation_pipeline)

    def load_llm(self, model_source, **kwargs):
        """
        加载 LLM 模型。

        参数：
        - model_source: 模型路径或名称。
        - kwargs: 其他可选参数，列表形式传递给 set_tokenizer 等，例如：
            - tokenizer_kwargs={"use_fast": True},
            - model_kwargs={"torch_dtype": "auto", device_map='auto', low_cpu_mem_usage=True},
            - pipeline_kwargs={"max_new_tokens": 512, truncation=True}
        """
        tokenizer_kwargs = kwargs.get("tokenizer_kwargs", {})
        model_kwargs = kwargs.get("model_kwargs", {})
        pipeline_kwargs = kwargs.get("pipeline_kwargs", {})

        # 设置 tokenizer 和模型
        self.set_tokenizer(model_source, **tokenizer_kwargs)
        self.set_model(model_source, **model_kwargs)

        # 设置 pipeline
        self.set_pipeline(**pipeline_kwargs)

    def load_embeddings(self, model_source, **kwargs):
        """
        加载 Embedding 模型。

        参数：
        - model_source: 模型路径或名称。
        - kwargs: 其他可选参数，用于传递给 HuggingFaceEmbeddings 方法。
        """
        if 'cuda' in self.devices[0]:
            embedding_device = 0  # 默认使用第一个 GPU 设备
        elif 'cpu' in self.devices:
            embedding_device = 'cpu'
        elif 'mps' in self.devices:
            embedding_device = 'mps'
        else:
            embedding_device = 'cpu'  # 默认使用 CPU

        # 创建 Embedding 模型
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_source,
            model_kwargs={'device': embedding_device},
            **kwargs
        )

    def get_llm(self):
        """返回加载的 LLM 模型对象。"""
        if self.llm_model is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm_model

    def get_embeddings(self):
        """返回加载的 Embedding 模型对象。"""
        if self.embedding_model is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.embedding_model