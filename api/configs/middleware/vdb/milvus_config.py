"""
Milvus 向量数据库配置

支持 Milvus 向量数据库连接和配置
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class MilvusConfig(BaseSettings):
    """
    Milvus 向量数据库配置
    """

    MILVUS_URI: Optional[str] = Field(
        description="连接到 Milvus 服务器的 URI（例如：'http://localhost:19530' 或 'https://milvus-instance.example.com:19530'）",
        default="http://127.0.0.1:19530",
    )

    MILVUS_TOKEN: Optional[str] = Field(
        description="Milvus 的认证令牌，如果启用了基于令牌的认证",
        default=None,
    )

    MILVUS_USER: Optional[str] = Field(
        description="用于 Milvus 认证的用户名，如果启用了用户名/密码认证",
        default=None,
    )

    MILVUS_PASSWORD: Optional[str] = Field(
        description="用于 Milvus 认证的密码，如果启用了用户名/密码认证",
        default=None,
    )

    MILVUS_DATABASE: str = Field(
        description="要连接的 Milvus 数据库名称（默认为 'default'）",
        default="default",
    )

    MILVUS_ENABLE_HYBRID_SEARCH: bool = Field(
        description="启用混合搜索功能（需要 Milvus >= 2.5.0）。设置为 false 以兼容旧版本",
        default=True,
    )

    MILVUS_ANALYZER_PARAMS: Optional[str] = Field(
        description='Milvus 文本分析器参数，例如 {"type": "chinese"} 用于中文分词支持。',
        default=None,
    )
