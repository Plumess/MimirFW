import requests
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.embeddings import Embeddings

class SentenceTransformersEmbeddings(BaseModel, Embeddings):
    """自定义的 Sentence Transformers Embeddings 类，通过 FastAPI 后端生成嵌入。

    参数：
        api_url (str): FastAPI 后端的 URL 地址。
        model_name (str): 后端使用的模型名称。
        model_kwargs (Dict[str, Any]): 模型加载时的参数。
        encode_kwargs (Dict[str, Any]): 编码时使用的其他关键字参数。
        multi_process (bool): 是否使用多进程。
        show_progress (bool): 是否在生成嵌入时显示进度。
    """

    api_url: str = "http://localhost:24101/embeddings/"
    model_name: str = "xiaobu-embedding-v2"
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    multi_process: bool = False
    show_progress: bool = False

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """通过向后端发送请求，为多个文本生成嵌入。

        参数：
            texts (List[str]): 需要生成嵌入的文本列表。

        返回：
            List[List[float]]: 每个文本对应的嵌入向量列表。
        """
        if not texts:
            raise ValueError("输入的文本列表为空，请提供至少一个文本。")

        payload = {
            "inputs": texts,
            "model_name": self.model_name,
            "model_kwargs": self.model_kwargs,
            "encode_kwargs": self.encode_kwargs,
            "multi_process": self.multi_process,
            "show_progress": self.show_progress,
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            embeddings = data.get("embeddings")
            if embeddings is None:
                raise ValueError("后端响应中没有 'embeddings' 字段。")
            return embeddings
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"HTTP 错误: {http_err}") from http_err
        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(f"请求后端时出错: {req_err}") from req_err
        except ValueError as val_err:
            raise RuntimeError(f"后端响应无效: {val_err}") from val_err

    def embed_query(self, text: str) -> List[float]:
        """为单个查询文本生成嵌入。

        参数：
            text (str): 需要生成嵌入的查询文本。

        返回：
            List[float]: 查询文本的嵌入向量。
        """
        if not text:
            raise ValueError("输入的文本为空，请提供有效的文本。")

        embeddings = self.embed_documents([text])
        return embeddings[0]

    model_config = ConfigDict(
        extra="forbid",  # 禁止传递未定义的字段
        protected_namespaces=(),  # 保护命名空间
        arbitrary_types_allowed=True
    )
    