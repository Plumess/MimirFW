"""
Weaviate 向量数据库配置

包含 Weaviate 连接、认证、批量操作等配置
"""

from typing import Optional

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class WeaviateConfig(BaseSettings):
    """
    Weaviate 向量数据库配置设置
    """

    WEAVIATE_ENDPOINT: Optional[str] = Field(
        description="Weaviate 服务器的 URL（例如：'http://localhost:8080' 或 'https://weaviate.example.com'）",
        default=None,
    )

    WEAVIATE_API_KEY: Optional[str] = Field(
        description="用于与 Weaviate 服务器认证的 API 密钥",
        default=None,
    )

    WEAVIATE_GRPC_ENABLED: bool = Field(
        description="是否启用 gRPC 进行 Weaviate 连接（True 为 gRPC，False 为 HTTP）",
        default=True,
    )

    WEAVIATE_BATCH_SIZE: PositiveInt = Field(
        description="单次批量操作中处理的对象数量（默认为 100）",
        default=100,
    )
