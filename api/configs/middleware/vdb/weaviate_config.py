"""
Weaviate 向量数据库配置
"""

from typing import Optional

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class WeaviateConfig(BaseSettings):
    """
    Weaviate 向量数据库配置
    """

    WEAVIATE_ENDPOINT: Optional[str] = Field(
        description="Weaviate 服务器的 URL（如 'http://localhost:8080' 或 'https://weaviate.example.com'）",
        default=None,
    )

    WEAVIATE_API_KEY: Optional[str] = Field(
        description="用于 Weaviate 服务器认证的 API 密钥",
        default=None,
    )

    WEAVIATE_GRPC_ENABLED: bool = Field(
        description="是否为 Weaviate 连接启用 gRPC（True 为 gRPC，False 为 HTTP）",
        default=True,
    )

    WEAVIATE_BATCH_SIZE: PositiveInt = Field(
        description="单次批处理操作中要处理的对象数量（默认为 100）",
        default=100,
    )
