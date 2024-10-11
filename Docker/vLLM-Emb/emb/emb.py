import os
import asyncio
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from sentence_transformers import SentenceTransformer

# 创建 FastAPI 应用实例
app = FastAPI()

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 模型缓存，用于避免重复加载模型
model_cache: Dict[str, SentenceTransformer] = {}

class EmbeddingRequest(BaseModel):
    """定义请求体的数据模型。"""
    inputs: List[str]
    model_name: str = "xiaobu-embedding-v2"
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    multi_process: bool = False
    show_progress: bool = False

    model_config = ConfigDict(
        extra="forbid",  # 禁止传递未定义的字段
        protected_namespaces=(),  # 保护命名空间
        arbitrary_types_allowed=True
    )


async def generate_embeddings(
    model: SentenceTransformer,
    texts: List[str],
    multi_process: bool = False,
    show_progress: bool = False,
    **encode_kwargs
):
    """异步生成嵌入的函数。

    参数：
        model (SentenceTransformer): 已加载的嵌入模型。
        texts (List[str]): 需要生成嵌入的文本列表。
        multi_process (bool): 是否使用多进程。
        show_progress (bool): 是否显示进度。
        encode_kwargs: 编码时的其他参数。

    返回：
        List[List[float]]: 嵌入向量列表。
    """
    loop = asyncio.get_event_loop()
    try:
        if multi_process:
            pool = model.start_multi_process_pool()
            embeddings = await loop.run_in_executor(
                None,
                lambda: model.encode_multi_process(texts, pool, **encode_kwargs)
            )
            model.stop_multi_process_pool(pool)
        else:
            embeddings = await loop.run_in_executor(
                None,
                lambda: model.encode(texts, show_progress_bar=show_progress, **encode_kwargs)
            )
        return embeddings.tolist()
    except Exception as e:
        raise RuntimeError(f"嵌入生成失败: {str(e)}")


def load_embedding_model(model_name: str, model_kwargs: Dict[str, Any]) -> SentenceTransformer:
    """加载指定名称的嵌入模型。

    参数：
        model_name (str): 模型名称。
        model_kwargs (Dict[str, Any]): 模型加载时的参数。

    返回：
        SentenceTransformer: 加载的模型实例。
    """
    if model_name in model_cache:
        return model_cache[model_name]

    model_path = os.path.join("/embeddings", model_name)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"模型路径 {model_path} 不存在")
    try:
        model = SentenceTransformer(model_path, **model_kwargs)
        model_cache[model_name] = model
        return model
    except Exception as e:
        raise RuntimeError(f"模型加载失败: {str(e)}")


@app.post("/embeddings/")
async def generate_embedding(request: EmbeddingRequest):
    """嵌入生成的 API 端点。

    参数：
        request (EmbeddingRequest): 请求体。

    返回：
        dict: 包含嵌入向量的响应。
    """
    try:
        logger.info(f"收到的请求: {request.dict()}")
        model = load_embedding_model(request.model_name, request.model_kwargs)

        if not request.inputs:
            raise ValueError("输入文本不能为空")

        embeddings = await generate_embeddings(
            model,
            request.inputs,
            multi_process=request.multi_process,
            show_progress=request.show_progress,
            **request.encode_kwargs
        )
        return {"embeddings": embeddings}

    except FileNotFoundError as fnfe:
        logger.error(f"模型未找到: {str(fnfe)}")
        raise HTTPException(status_code=404, detail=f"模型未找到: {str(fnfe)}")
    except ValueError as ve:
        logger.error(f"无效输入: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"无效输入: {str(ve)}")
    except Exception as e:
        logger.error(f"内部服务器错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")
    