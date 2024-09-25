from abc import ABC, abstractmethod
from LLMCore.managers.inference_framework import *
from config import PROJECT_ROOT

# ==============================
# 模型加载器调用接口类
# ==============================
class ModelLoaderInterface:
    def __init__(self, model_type='local', inference_framework_type='vllm'):
        """
        初始化模型加载器接口。

        参数：
        - model_type: 模型类型，'local' 或 'api'。
        - inference_framework_type: 推理框架/供应商标识符。
            若模型为本地，则支持 'vllm'、'transformers' 等;
            若模型为 API 获得，则支持 'openai', 'qwen';
        """
        self.model_type = model_type.lower()
        self.inference_framework_type = inference_framework_type.lower()
        # device_info: 设备信息，默认自动获取。
        from config import DEVICE_INFO
        self.device_info = DEVICE_INFO

        # 初始化模型路径或标识符
        self.llm_model_source = None
        self.embedding_model_source = None

        # 初始化模型加载器
        self.loader = None

    def set_llm_model_source(self, llm_model_source):
        """设置 LLM 模型路径或标识符，并创建或更新模型加载器。"""
        self.llm_model_source = llm_model_source
        self._create_or_update_model_loader()

    def set_embedding_model_source(self, embedding_model_source):
        """设置 Embedding 模型路径或标识符，并创建或更新模型加载器。"""
        self.embedding_model_source = embedding_model_source
        self._create_or_update_model_loader()

    def _create_or_update_model_loader(self):
        """根据模型路径和其他参数创建或更新模型加载器实例。"""
        if not self.llm_model_source and not self.embedding_model_source:
            # 如果两个模型路径都未设置，不创建模型加载器
            return

        if self.model_type == 'local':
            if self.device_info['GPU']['CUDA']:
                # 使用 CUDA 模型加载器
                self.loader = CUDAModelLoader(
                    llm_model_source=self.llm_model_source,
                    embedding_model_source=self.embedding_model_source,
                    inference_framework_type=self.inference_framework_type,
                    device_info=self.device_info
                )
            elif self.device_info['GPU']['MPS']:
                # 使用 Mac 平台模型加载器
                self.loader = MacModelLoader(
                    llm_model_source=self.llm_model_source,
                    embedding_model_source=self.embedding_model_source,
                    inference_framework_type=self.inference_framework_type,
                    device_info=self.device_info
                )
            else:
                # 使用 CPU 模型加载器
                self.loader = CPUModelLoader(
                    llm_model_source=self.llm_model_source,
                    embedding_model_source=self.embedding_model_source,
                    inference_framework_type=self.inference_framework_type,
                    device_info=self.device_info
                )
        elif self.model_type == 'api':
            # 使用 API 模型加载器
            self.loader = APIModelLoader(
                llm_model_source=self.llm_model_source,
                embedding_model_source=self.embedding_model_source,
                inference_framework_type=self.inference_framework_type
            )
        else:
            raise ValueError(f"不支持的模型类型：{self.model_type}")

    def load_llm(self, **llm_kwargs):
        """加载 LLM 模型。此处的 kwargs 为模型加载特有的参数。"""
        if self.loader is None:
            raise ValueError("请先设置 LLM 模型路径, set_llm_model_source(llm_model_source)")
        self.loader.load_llm(**llm_kwargs)

    def load_embeddings(self, **embeddings_kwargs):
        """加载 Embedding 模型。此处的 kwargs 为模型加载特有的参数。"""
        if self.loader is None:
            raise ValueError("请先设置 Embedding 模型路径, set_embedding_model_source(embedding_model_source)")
        self.loader.load_embeddings(**embeddings_kwargs)

    def get_llm(self):
        """获取与 LangChain 兼容的 LLM 对象。"""
        if self.loader is None:
            raise ValueError("LLM 模型尚未加载")
        return self.loader.get_llm()

    def get_embeddings(self):
        """获取 Embedding 模型对象。"""
        if self.loader is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.loader.get_embeddings()


# ==============================
# 模型加载器基类
# ==============================
class ModelLoader(ABC):
    def __init__(self, llm_model_source=None, embedding_model_source=None, inference_framework_type=None, device_info=None):
        """
        初始化模型加载器。

        参数：
        - llm_model_source: LLM 模型路径或标识符。
        - embedding_model_source: Embedding 模型路径或标识符。
        - inference_framework_type: 推理框架/供应商标识符。
        - device_info: 设备信息, 由Interface自动获取并传入。
        """
        self.llm_model_source = llm_model_source
        self.embedding_model_source = embedding_model_source
        self.inference_framework_type = inference_framework_type
        self.device_info = device_info

        self.inference_framework = None  # 存储实际调用的推理框架类
        self.llm = None  # 存储加载的 LLM 模型
        self.embeddings = None  # 存储加载的 Embedding 模型

    @abstractmethod
    def load_llm(self, **llm_kwargs):
        """加载 LLM 模型，由子类实现。"""
        pass

    @abstractmethod
    def load_embeddings(self, **embeddings_kwargs):
        """加载 Embedding 模型，由子类实现。"""
        pass

    def get_llm(self):
        """获取与 LangChain 兼容的 LLM 对象。"""
        if self.llm is None:
            raise ValueError("LLM 模型尚未加载")
        return self.llm

    def get_embeddings(self):
        """获取 Embedding 模型对象。"""
        if self.embeddings is None:
            raise ValueError("Embedding 模型尚未加载")
        return self.embeddings


# ==============================
# API 模型加载器子类
# ==============================
class APIModelLoader(ModelLoader):
    def __init__(self, llm_model_source=None, embedding_model_source=None, inference_framework_type='openai'):
        """
        初始化 API 模型加载器。暂时支持使用 Open AI SDK 的供应商：OpenAI, Qwen

        参数：
        - llm_model_source: 官方给出的 LLM 模型标识符（例如，'gpt-3.5-turbo', 'qwen2.5-72b-instruct'）。
        - embedding_model_source: Embedding 模型标识符（例如，'text-embedding-3-small', 'text-embedding-v3'）。
        - inference_framework_type: 推理 API 供应商，'openai'、'qwen' 等。
        """
        super().__init__(llm_model_source, embedding_model_source, inference_framework_type)

        # 根据推理框架初始化对应的推理引擎
        if inference_framework_type == 'openai':
            self.inference_framework = OpenAIAPIFramework()
        elif inference_framework_type == 'qwen':
            self.inference_framework = QwenAPIFramework()
        else:
            raise ValueError(f"暂时支持使用 OpenAI SDK 的供应商：OpenAI, Qwen。暂不支持所设置推理框架：{inference_framework_type}")

    def load_llm(self, **llm_kwargs):
        if not self.llm_model_source:
            raise ValueError("LLM 模型标识符未设置")
        self.inference_framework.load_llm(self.llm_model_source, **llm_kwargs)
        self.llm = self.inference_framework.get_llm()

    def load_embeddings(self, **embeddings_kwargs):
        if not self.embedding_model_source:
            raise ValueError("Embedding 模型标识符未设置")
        self.inference_framework.load_embeddings(self.embedding_model_source, **embeddings_kwargs)
        self.embeddings = self.inference_framework.get_embeddings()


# ==============================
# CUDA 模型加载器子类
# ==============================
class CUDAModelLoader(ModelLoader):
    def __init__(self, llm_model_source=None, embedding_model_source=None, inference_framework_type='vllm', device_info=None):
        super().__init__(llm_model_source, embedding_model_source, inference_framework_type, device_info)

        if self.inference_framework_type == 'vllm':
            # 初始化 VLLMFramework
            self.inference_framework = VLLMFramework()

        elif self.inference_framework_type == 'transformers':
            # 使用本地 Transformers 框架
            if self.device_info is None:
                from config import DEVICE_INFO
                self.device_info = DEVICE_INFO

            device_ids = [device['Device Index'] for device in self.device_info['GPU']['CUDA Devices']]
            if not device_ids:
                raise ValueError("没有可用的 CUDA 设备")

            self.device_ids = device_ids
            self.device = f'cuda:{device_ids[0]}'

            self.inference_framework = TransformersFramework(device=self.device)
        else:
            raise ValueError(f"不支持的推理框架：{self.inference_framework_type}")

    def load_llm(self, **llm_kwargs):
        """加载 LLM 模型，kwargs 包含模型加载特有的参数。"""
        if not self.llm_model_source:
            raise ValueError("LLM 模型标识符未设置")
        self.inference_framework.load_llm(self.llm_model_source, **llm_kwargs)
        self.llm = self.inference_framework.get_llm()

    def load_embeddings(self, **embeddings_kwargs):
        """加载 Embedding 模型，kwargs 包含模型加载特有的参数。"""
        if not self.embedding_model_source:
            raise ValueError("Embedding 模型标识符未设置")
        self.inference_framework.load_embeddings(self.embedding_model_source, **embeddings_kwargs)
        self.embeddings = self.inference_framework.get_embeddings()


# ==============================
# CPU 模型加载器子类（未测试）
# ==============================
class CPUModelLoader(ModelLoader):
    def __init__(self, llm_model_source=None, embedding_model_source=None, inference_framework_type='vllm', device_info=None):
        super().__init__(llm_model_source, embedding_model_source, inference_framework_type, device_info)

        if self.inference_framework_type == 'vllm':
            # 初始化 VLLMFramework，不需要传递 base_url
            self.inference_framework = VLLMFramework()

        elif self.inference_framework_type == 'transformers':
            # 使用本地 Transformers 框架
            self.device = 'cpu'
            self.inference_framework = TransformersFramework(device=self.device)
        else:
            raise ValueError(f"不支持的推理框架：{self.inference_framework_type}")

    def load_llm(self, **llm_kwargs):
        """加载 LLM 模型，kwargs 包含模型加载特有的参数。"""
        if not self.llm_model_source:
            raise ValueError("LLM 模型标识符未设置")
        self.inference_framework.load_llm(self.llm_model_source, **llm_kwargs)
        self.llm = self.inference_framework.get_llm()

    def load_embeddings(self, **embeddings_kwargs):
        """加载 Embedding 模型，kwargs 包含模型加载特有的参数。"""
        if not self.embedding_model_source:
            raise ValueError("Embedding 模型标识符未设置")
        self.inference_framework.load_embeddings(self.embedding_model_source, **embeddings_kwargs)
        self.embeddings = self.inference_framework.get_embeddings()

# ==============================
# Mac 模型加载器子类（未完成）
# ==============================
class MacModelLoader(ModelLoader):
    def __init__(self, llm_model_source=None, embedding_model_source=None, inference_framework_type='transformers', device_info=None):
        super().__init__(llm_model_source, embedding_model_source, inference_framework_type, device_info)

        self.device = 'mps'

        # 根据推理框架初始化对应的推理引擎
        if self.inference_framework_type == 'transformers':
            self.inference_framework = TransformersFramework(device=self.device)
            
        elif self.inference_framework_type == 'mlx':
            raise NotImplementedError("MLX 推理引擎未实现")
        else:
            raise ValueError(f"不支持的推理框架：{self.inference_framework_type}")

    def load_llm(self, **llm_kwargs):
        if not self.llm_model_source:
            raise ValueError("LLM 模型路径未设置")
        self.inference_framework.load_llm(self.llm_model_source, **llm_kwargs)
        self.llm = self.inference_framework.get_llm()

    def load_embeddings(self, **embeddings_kwargs):
        if not self.embedding_model_source:
            raise ValueError("Embedding 模型路径未设置")
        self.inference_framework.load_embeddings(self.embedding_model_source, **embeddings_kwargs)
        self.embeddings = self.inference_framework.get_embeddings()
