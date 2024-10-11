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

# 引用 VLLM_SERVER_BASE_URL, EMBEDDING_SERVER_BASE_URL 等地址变量
from config import *

class VLLMFramework(InferenceFramework):
    def __init__(self):
        """
        初始化 VLLM 推理接口。
        """
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, llm_model_source, **llm_kwargs):
        """
        使用 LangChain VLLM OpenAI 集成接口 调用后端 加载 LLM 模型
        """
        from langchain_openai import ChatOpenAI

        self.llm_model = ChatOpenAI(
            model=f'/models/{llm_model_source}',
            openai_api_key="EMPTY",
            openai_api_base=VLLM_SERVER_BASE_URL,
            **llm_kwargs
            # 例如
            # max_tokens=512,
            # temperature=0.8,
        )

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        """
        暂时使用 huggingface 接口加载 Embeddings 模型。

        参数：
        - model_source: 模型路径或名称。
        - kwargs: 其他可选参数，用于传递给 HuggingFaceEmbeddings 方法。
        """

        from LLMCore.customs.langchain_embeddings import SentenceTransformersEmbeddings

        # 创建 Embedding 模型
        self.embedding_model = SentenceTransformersEmbeddings(
            model_name=embeddings_model_source,  # 本地模型名称
            api_url=EMBEDDING_SERVER_BASE_URL  # 自定义的 FastAPI URL
            # 其他支持的参数
        )

    def get_llm(self):
        if self.llm_model is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm_model

    def get_embeddings(self):
        if self.embedding_model is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.embedding_model