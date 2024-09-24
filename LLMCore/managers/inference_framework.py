from abc import ABC, abstractmethod
from config import QWEN_BASE_URL
import os

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
# 通用 API 推理引擎基类
# ==============================
class BaseAPIFramework(InferenceFramework):
    def __init__(self):
        """
        初始化 API 推理引擎基类。
        """
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, llm_model_source, **llm_kwargs):
        """
        加载通用 LLM 模型，子类可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_openai import ChatOpenAI

        self.llm_api_key = llm_kwargs.pop('api_key', os.getenv('API_KEY'))
        if not self.llm_api_key:
            raise ValueError("LLM API 密钥未设置")

        # 如果子类需要，可以覆盖 base_url
        self.llm_base_url = llm_kwargs.pop('base_url', None)

        self.llm_model = ChatOpenAI(
            model=llm_model_source,
            api_key=self.llm_api_key,
            base_url=self.llm_base_url,
            **llm_kwargs
        )

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        """
        加载通用 Embeddings 模型，子类可根据需要覆盖 base_url 或其他参数。
        """
        from langchain_openai import OpenAIEmbeddings

        self.embeddings_api_key = embeddings_kwargs.pop('api_key', os.getenv('API_KEY'))
        if not self.embeddings_api_key:
            raise ValueError("Embeddings API 密钥未设置")

        # 如果子类需要，可以覆盖 base_url
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
# OpenAI API 推理引擎
# ==============================
class OpenAIAPIFramework(BaseAPIFramework):
    def __init__(self):
        """
        初始化 OpenAI API 推理引擎。
        """
        super().__init__()


# ==============================
# 阿里云 Qwen2 API 推理引擎
# ==============================
class QwenAPIFramework(BaseAPIFramework):
    def __init__(self):
        """
        初始化 Qwen API 推理引擎。
        """
        super().__init__()

    def load_llm(self, llm_model_source, **llm_kwargs):
        # 若用户未设置 base_url，则使用 Qwen 官方默认的 base_url
        if 'base_url' not in llm_kwargs:
            llm_kwargs['base_url'] = QWEN_BASE_URL

        # 调用基类的方法进行加载
        super().load_llm(llm_model_source, **llm_kwargs)

    def load_embeddings(self, embeddings_model_source, **embeddings_kwargs):
        # 若用户未设置 base_url，则使用 Qwen 官方默认的 base_url
        if 'base_url' not in embeddings_kwargs:
            embeddings_kwargs['base_url'] = QWEN_BASE_URL

        # 调用基类的方法进行加载
        super().load_embeddings(embeddings_model_source, **embeddings_kwargs)


# ==============================
# VLLM 推理引擎实现（适用于 CUDA）（未完成）
# ==============================
class VLLMFramework(InferenceFramework):
    def __init__(self, device_type='cuda', device_ids=None):
        """
        初始化 VLLM 推理引擎。

        参数：
        - device_type: 'cpu' 或 'cuda'。
        - device_ids: CUDA 设备索引列表，CPU 时为 None。
        """
        self.device_type = device_type
        self.device_ids = device_ids
        self.llm_model = None

    def load_llm(self, model_source, **kwargs):
        from langchain.llms import VLLM

        if self.device_type == 'cuda':
            tensor_parallel_size = len(self.device_ids) if self.device_ids else 1
            self.llm_model = VLLM(
                model=model_source,
                tensor_parallel_size=tensor_parallel_size,
                **kwargs
            )
        elif self.device_type == 'cpu':
            self.llm_model = VLLM(
                model=model_source,
                tensor_parallel_size=1,
                **kwargs
            )
        else:
            raise ValueError(f"不支持的设备类型：{self.device_type}")

    def load_embeddings(self, model_source, **kwargs):
        # VLLM 目前不支持 Embedding，如需支持可在此实现
        raise NotImplementedError("VLLM 推理引擎暂不支持 Embedding 模型的加载。")

    def get_llm(self):
        if self.llm_model is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm_model

    def get_embeddings(self):
        raise NotImplementedError("VLLM 推理引擎暂不支持 Embedding 模型的加载。")

    
# ==============================
# Huggingface Transformers （通用）（未完成）
# ==============================
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings

class TransformersFramework(InferenceFramework):
    def __init__(self, device):
        """
        初始化 Transformers 推理引擎。

        参数：
        - device: 设备名称，如 'cpu'、'cuda:0'、'mps' 等。
        """
        self.device = device
        self.llm_model = None
        self.embedding_model = None

    def load_llm(self, model_source, **kwargs):
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

        tokenizer = AutoTokenizer.from_pretrained(model_source, **kwargs)
        model = AutoModelForCausalLM.from_pretrained(model_source, **kwargs)
        model.to(self.device)

        # 根据设备类型设置 pipeline 的 device 参数
        if 'cuda' in self.device:
            device = int(self.device.split(':')[-1])
        elif 'cpu' in self.device:
            device = -1
        elif 'mps' in self.device:
            device = -1  # MPS 设备暂时使用 -1，transformers 会自动检测
        else:
            device = -1

        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device,
            **kwargs
        )

        self.llm_model = HuggingFacePipeline(pipeline=generation_pipeline)

    def load_embeddings(self, model_source, **kwargs):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_source,
            model_kwargs={"device": self.device},
            **kwargs
        )

    def get_llm(self):
        if self.llm_model is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm_model

    def get_embeddings(self):
        if self.embedding_model is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.embedding_model

